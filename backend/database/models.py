from database.db_config import get_db_connection
from utils.auth_utils import hash_password, check_password
from datetime import datetime
import traceback

class User:
    @staticmethod
    def create(username, email, password, first_name, last_name, user_type):
        """Create a new user"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            password_hash = hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, email, password_hash, first_name, last_name, user_type))
            
            user_id = cursor.lastrowid
            
            # Create profile based on user type
            if user_type == 'freelancer':
                cursor.execute("""
                    INSERT INTO freelancer_profiles (user_id)
                    VALUES (%s)
                """, (user_id,))
            else:
                cursor.execute("""
                    INSERT INTO recruiter_profiles (user_id, company_name)
                    VALUES (%s, %s)
                """, (user_id, f"{first_name} {last_name}'s Company"))
            
            connection.commit()
            print(f"✅ User created successfully with ID: {user_id}")
            return user_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating user: {str(e)}")
            traceback.print_exc()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, first_name, last_name, 
                       user_type, is_active, is_verified, date_joined, profile_picture
                FROM users WHERE email = %s
            """, (email,))
            
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"❌ Error finding user by email: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT id, username, email, first_name, last_name, 
                       user_type, is_active, is_verified, date_joined, profile_picture
                FROM users WHERE id = %s
            """, (user_id,))
            
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"❌ Error finding user by ID: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user"""
        try:
            user = User.find_by_email(email)
            if user and check_password(password, user['password_hash']):
                # Update last login
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users SET last_login = NOW() WHERE id = %s
                """, (user['id'],))
                connection.commit()
                cursor.close()
                connection.close()
                
                # Remove password hash before returning
                user_dict = dict(user)
                del user_dict['password_hash']
                return user_dict
            return None
        except Exception as e:
            print(f"❌ Error authenticating user: {str(e)}")
            return None
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login timestamp"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE users SET last_login = NOW() WHERE id = %s
            """, (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"❌ Error updating last login: {str(e)}")
            return False

class FreelancerProfile:
    @staticmethod
    def get_by_user_id(user_id):
        """Get freelancer profile by user ID"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
                       u.profile_picture as user_profile_picture
                FROM freelancer_profiles fp
                JOIN users u ON fp.user_id = u.id
                WHERE fp.user_id = %s
            """, (user_id,))
            
            profile = cursor.fetchone()
            
            if profile:
                # Convert to dict if it's not already
                profile = dict(profile)
                
                # Get skills
                cursor.execute("""
                    SELECT s.id, s.name, fs.proficiency_level
                    FROM freelancer_skills fs
                    JOIN skills s ON fs.skill_id = s.id
                    WHERE fs.freelancer_profile_id = %s
                """, (profile['id'],))
                profile['skills'] = [dict(skill) for skill in cursor.fetchall()]
                
                # Get tech stacks
                cursor.execute("""
                    SELECT ts.id, ts.name, fts.experience_years
                    FROM freelancer_tech_stacks fts
                    JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
                    WHERE fts.freelancer_profile_id = %s
                """, (profile['id'],))
                profile['tech_stacks'] = [dict(tech) for tech in cursor.fetchall()]
            
            return profile
        except Exception as e:
            print(f"❌ Error getting freelancer profile: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def update_profile(user_id, profile_data):
        """Update freelancer profile"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get profile ID
            cursor.execute("""
                SELECT id FROM freelancer_profiles WHERE user_id = %s
            """, (user_id,))
            profile = cursor.fetchone()
            
            if not profile:
                print(f"❌ Freelancer profile not found for user {user_id}")
                return None
            
            profile_id = profile['id']
            
            # Update basic profile fields
            update_fields = []
            values = []
            
            allowed_fields = ['bio', 'hourly_rate', 'education', 'experience', 
                             'years_of_experience', 'github_url', 'linkedin_url', 
                             'portfolio_url', 'is_available']
            
            for field in allowed_fields:
                if field in profile_data:
                    update_fields.append(f"{field} = %s")
                    values.append(profile_data[field])
            
            if update_fields:
                values.append(profile_id)
                query = f"""
                    UPDATE freelancer_profiles 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, values)
            
            # Update skills
            if 'skills' in profile_data:
                # Delete existing skills
                cursor.execute("""
                    DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s
                """, (profile_id,))
                
                # Add new skills
                for skill in profile_data['skills']:
                    # Check if skill exists
                    skill_name = skill.get('name') if isinstance(skill, dict) else skill
                    cursor.execute("""
                        SELECT id FROM skills WHERE name = %s
                    """, (skill_name,))
                    skill_record = cursor.fetchone()
                    
                    if skill_record:
                        skill_id = skill_record['id']
                    else:
                        # Create new skill
                        cursor.execute("""
                            INSERT INTO skills (name) VALUES (%s)
                        """, (skill_name,))
                        skill_id = cursor.lastrowid
                    
                    proficiency = skill.get('proficiency_level', 'intermediate') if isinstance(skill, dict) else 'intermediate'
                    
                    # Add to freelancer_skills
                    cursor.execute("""
                        INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
                        VALUES (%s, %s, %s)
                    """, (profile_id, skill_id, proficiency))
            
            # Update tech stacks
            if 'tech_stacks' in profile_data:
                # Delete existing tech stacks
                cursor.execute("""
                    DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s
                """, (profile_id,))
                
                # Add new tech stacks
                for tech in profile_data['tech_stacks']:
                    tech_name = tech.get('name') if isinstance(tech, dict) else tech
                    
                    # Check if tech stack exists
                    cursor.execute("""
                        SELECT id FROM tech_stacks WHERE name = %s
                    """, (tech_name,))
                    tech_record = cursor.fetchone()
                    
                    if tech_record:
                        tech_id = tech_record['id']
                    else:
                        # Create new tech stack
                        cursor.execute("""
                            INSERT INTO tech_stacks (name) VALUES (%s)
                        """, (tech_name,))
                        tech_id = cursor.lastrowid
                    
                    experience = tech.get('experience_years', 0) if isinstance(tech, dict) else 0
                    
                    # Add to freelancer_tech_stacks
                    cursor.execute("""
                        INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
                        VALUES (%s, %s, %s)
                    """, (profile_id, tech_id, experience))
            
            connection.commit()
            print(f"✅ Freelancer profile updated for user {user_id}")
            
            return FreelancerProfile.get_by_user_id(user_id)
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating freelancer profile: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def search_freelancers(filters):
        """Search freelancers based on skills, rate, experience"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
                       u.date_joined
                FROM freelancer_profiles fp
                JOIN users u ON fp.user_id = u.id
                WHERE u.is_active = TRUE AND fp.is_available = TRUE
            """
            params = []
            
            if filters.get('min_hourly_rate'):
                query += " AND fp.hourly_rate >= %s"
                params.append(filters['min_hourly_rate'])
            
            if filters.get('max_hourly_rate'):
                query += " AND fp.hourly_rate <= %s"
                params.append(filters['max_hourly_rate'])
            
            if filters.get('years_experience_min'):
                query += " AND fp.years_of_experience >= %s"
                params.append(filters['years_experience_min'])
            
            if filters.get('skill'):
                query += """ AND fp.id IN (
                    SELECT fs.freelancer_profile_id 
                    FROM freelancer_skills fs
                    JOIN skills s ON fs.skill_id = s.id
                    WHERE s.name LIKE %s
                )"""
                params.append(f'%{filters["skill"]}%')
            
            query += " ORDER BY fp.created_at DESC LIMIT 50"
            
            cursor.execute(query, params)
            freelancers = cursor.fetchall()
            
            # Get skills and tech stacks for each freelancer
            result = []
            for freelancer in freelancers:
                freelancer = dict(freelancer)
                
                # Get skills
                cursor.execute("""
                    SELECT s.id, s.name, fs.proficiency_level
                    FROM freelancer_skills fs
                    JOIN skills s ON fs.skill_id = s.id
                    WHERE fs.freelancer_profile_id = %s
                """, (freelancer['id'],))
                freelancer['skills'] = [dict(skill) for skill in cursor.fetchall()]
                
                # Get tech stacks
                cursor.execute("""
                    SELECT ts.id, ts.name, fts.experience_years
                    FROM freelancer_tech_stacks fts
                    JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
                    WHERE fts.freelancer_profile_id = %s
                """, (freelancer['id'],))
                freelancer['tech_stacks'] = [dict(tech) for tech in cursor.fetchall()]
                
                result.append(freelancer)
            
            return result
        except Exception as e:
            print(f"❌ Error searching freelancers: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class RecruiterProfile:
    @staticmethod
    def get_by_user_id(user_id):
        """Get recruiter profile by user ID"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT rp.*, u.username, u.email, u.first_name, u.last_name
                FROM recruiter_profiles rp
                JOIN users u ON rp.user_id = u.id
                WHERE rp.user_id = %s
            """, (user_id,))
            
            profile = cursor.fetchone()
            if profile:
                profile = dict(profile)
            return profile
        except Exception as e:
            print(f"❌ Error getting recruiter profile: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def update_profile(user_id, profile_data):
        """Update recruiter profile"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            update_fields = []
            values = []
            
            allowed_fields = ['company_name', 'company_website', 'company_size', 
                             'industry', 'company_description', 'location', 'phone']
            
            for field in allowed_fields:
                if field in profile_data:
                    update_fields.append(f"{field} = %s")
                    values.append(profile_data[field])
            
            if update_fields:
                values.append(user_id)
                query = f"""
                    UPDATE recruiter_profiles 
                    SET {', '.join(update_fields)}
                    WHERE user_id = %s
                """
                cursor.execute(query, values)
                connection.commit()
                print(f"✅ Recruiter profile updated for user {user_id}")
            
            return RecruiterProfile.get_by_user_id(user_id)
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating recruiter profile: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class Job:
    @staticmethod
    def create(recruiter_id, job_data):
        """Create a new job posting"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get recruiter profile ID
            cursor.execute("""
                SELECT id FROM recruiter_profiles WHERE user_id = %s
            """, (recruiter_id,))
            profile = cursor.fetchone()
            
            if not profile:
                print(f"❌ Recruiter profile not found for user {recruiter_id}")
                return None
            
            # Insert job
            cursor.execute("""
                INSERT INTO jobs (
                    recruiter_id, recruiter_profile_id, title, description,
                    pay_per_hour, experience_level, job_type, location,
                    is_remote, requirements, responsibilities, benefits,
                    application_deadline
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                recruiter_id, profile['id'], job_data['title'],
                job_data['description'], job_data['pay_per_hour'],
                job_data['experience_level'], job_data.get('job_type', 'freelance'),
                job_data.get('location'), job_data.get('is_remote', True),
                job_data.get('requirements'), job_data.get('responsibilities'),
                job_data.get('benefits'), job_data.get('application_deadline')
            ))
            
            job_id = cursor.lastrowid
            print(f"✅ Job created with ID: {job_id}")
            
            # Add required skills
            if 'required_skills' in job_data and job_data['required_skills']:
                for skill_name in job_data['required_skills']:
                    # Get or create skill
                    cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
                    skill = cursor.fetchone()
                    if skill:
                        skill_id = skill['id']
                    else:
                        cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
                        skill_id = cursor.lastrowid
                    
                    cursor.execute("""
                        INSERT INTO job_skills (job_id, skill_id, is_required)
                        VALUES (%s, %s, TRUE)
                    """, (job_id, skill_id))
                    print(f"  Added skill: {skill_name}")
            
            # Add tech stack
            if 'tech_stack' in job_data and job_data['tech_stack']:
                for tech_name in job_data['tech_stack']:
                    # Get or create tech stack
                    cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
                    tech = cursor.fetchone()
                    if tech:
                        tech_id = tech['id']
                    else:
                        cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
                        tech_id = cursor.lastrowid
                    
                    cursor.execute("""
                        INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
                        VALUES (%s, %s, TRUE)
                    """, (job_id, tech_id))
                    print(f"  Added tech: {tech_name}")
            
            connection.commit()
            return job_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating job: {str(e)}")
            traceback.print_exc()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_by_id(job_id):
        """Get job by ID"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT j.*, rp.company_name, u.email as recruiter_email,
                       CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
                FROM jobs j
                JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
                JOIN users u ON j.recruiter_id = u.id
                WHERE j.id = %s
            """, (job_id,))
            
            job = cursor.fetchone()
            
            if job:
                job = dict(job)
                
                # Get required skills
                cursor.execute("""
                    SELECT s.id, s.name
                    FROM job_skills js
                    JOIN skills s ON js.skill_id = s.id
                    WHERE js.job_id = %s AND js.is_required = TRUE
                """, (job_id,))
                job['required_skills'] = [s['name'] for s in cursor.fetchall()]
                
                # Get tech stack
                cursor.execute("""
                    SELECT ts.id, ts.name
                    FROM job_tech_stacks jts
                    JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
                    WHERE jts.job_id = %s AND jts.is_required = TRUE
                """, (job_id,))
                job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
                
                # Increment view count
                cursor.execute("""
                    UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
                """, (job_id,))
                connection.commit()
                print(f"👁️ Job {job_id} view count incremented")
            
            return job
        except Exception as e:
            print(f"❌ Error getting job by ID: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def search_jobs(filters):
        """Search jobs with filters"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                SELECT j.*, rp.company_name,
                       CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
                FROM jobs j
                JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
                JOIN users u ON j.recruiter_id = u.id
                WHERE j.is_active = TRUE
            """
            params = []
            
            # IMPROVED SEARCH: Case-insensitive search with better matching
            if filters.get('search'):
                search_term = f'%{filters["search"]}%'
                query += """ AND (
                    LOWER(j.title) LIKE LOWER(%s) OR 
                    LOWER(j.description) LIKE LOWER(%s) OR 
                    LOWER(j.requirements) LIKE LOWER(%s) OR
                    LOWER(j.title) LIKE LOWER(%s)
                )"""
                params.extend([search_term, search_term, search_term, search_term])
                print(f"🔍 Searching with term: {filters['search']}")
            
            if filters.get('experience_level'):
                query += " AND j.experience_level = %s"
                params.append(filters['experience_level'])
            
            if filters.get('min_pay'):
                try:
                    min_pay = float(filters['min_pay'])
                    query += " AND j.pay_per_hour >= %s"
                    params.append(min_pay)
                except (ValueError, TypeError):
                    pass
            
            if filters.get('max_pay'):
                try:
                    max_pay = float(filters['max_pay'])
                    query += " AND j.pay_per_hour <= %s"
                    params.append(max_pay)
                except (ValueError, TypeError):
                    pass
            
            if filters.get('job_type'):
                query += " AND j.job_type = %s"
                params.append(filters['job_type'])
            
            if filters.get('is_remote'):
                query += " AND j.is_remote = TRUE"
            
            query += " ORDER BY j.created_at DESC"
            
            print(f"📝 Executing query: {query}")
            print(f"📝 With params: {params}")
            
            cursor.execute(query, params)
            jobs = cursor.fetchall()
            
            print(f"✅ Found {len(jobs)} jobs")
            
            # Get skills and tech stack for each job
            result = []
            for job in jobs:
                job = dict(job)
                
                cursor.execute("""
                    SELECT s.name
                    FROM job_skills js
                    JOIN skills s ON js.skill_id = s.id
                    WHERE js.job_id = %s
                """, (job['id'],))
                job['required_skills'] = [s['name'] for s in cursor.fetchall()]
                
                cursor.execute("""
                    SELECT ts.name
                    FROM job_tech_stacks jts
                    JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
                    WHERE jts.job_id = %s
                """, (job['id'],))
                job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
                
                result.append(job)
            
            return result
        except Exception as e:
            print(f"❌ Error searching jobs: {str(e)}")
            traceback.print_exc()
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_by_recruiter(recruiter_id):
        """Get all jobs posted by a recruiter"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT j.*, 
                       (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as total_applications
                FROM jobs j
                WHERE j.recruiter_id = %s
                ORDER BY j.created_at DESC
            """, (recruiter_id,))
            
            jobs = cursor.fetchall()
            result = [dict(job) for job in jobs]
            return result
        except Exception as e:
            print(f"❌ Error getting jobs by recruiter: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class JobApplication:
    @staticmethod
    def create(job_id, freelancer_id, application_data):
        """Create a new job application"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Check if already applied
            cursor.execute("""
                SELECT id FROM job_applications 
                WHERE job_id = %s AND freelancer_id = %s
            """, (job_id, freelancer_id))
            
            if cursor.fetchone():
                print(f"⚠️ Freelancer {freelancer_id} already applied to job {job_id}")
                return None
            
            # Get freelancer profile ID
            cursor.execute("""
                SELECT id FROM freelancer_profiles WHERE user_id = %s
            """, (freelancer_id,))
            profile = cursor.fetchone()
            
            if not profile:
                print(f"❌ Freelancer profile not found for user {freelancer_id}")
                return None
            
            # Create application
            cursor.execute("""
                INSERT INTO job_applications (
                    job_id, freelancer_id, freelancer_profile_id,
                    cover_letter, proposed_rate, availability_date
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                job_id, freelancer_id, profile['id'],
                application_data.get('cover_letter'),
                application_data.get('proposed_rate'),
                application_data.get('availability_date')
            ))
            
            application_id = cursor.lastrowid
            
            # Update job applications count
            cursor.execute("""
                UPDATE jobs SET applications_count = applications_count + 1
                WHERE id = %s
            """, (job_id,))
            
            connection.commit()
            print(f"✅ Application {application_id} created for job {job_id}")
            return application_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating application: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def update_status(application_id, status, recruiter_notes=None):
        """Update application status"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get application details
            cursor.execute("""
                SELECT ja.*, j.title, j.recruiter_id, 
                       u.email as freelancer_email,
                       CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN users u ON ja.freelancer_id = u.id
                WHERE ja.id = %s
            """, (application_id,))
            
            application = cursor.fetchone()
            
            if not application:
                print(f"❌ Application {application_id} not found")
                return None
            
            # Update status with timestamp
            timestamp_field = {
                'reviewed': 'reviewed_at',
                'accepted': 'accepted_at',
                'rejected': 'rejected_at'
            }.get(status)
            
            if timestamp_field:
                cursor.execute(f"""
                    UPDATE job_applications 
                    SET status = %s, recruiter_notes = %s, {timestamp_field} = NOW()
                    WHERE id = %s
                """, (status, recruiter_notes, application_id))
            else:
                cursor.execute("""
                    UPDATE job_applications 
                    SET status = %s, recruiter_notes = %s
                    WHERE id = %s
                """, (status, recruiter_notes, application_id))
            
            connection.commit()
            print(f"✅ Application {application_id} status updated to {status}")
            return dict(application)
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating application status: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_by_job(job_id):
        """Get all applications for a job"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT ja.*, 
                       fp.hourly_rate, fp.years_of_experience,
                       CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
                       u.email as freelancer_email
                FROM job_applications ja
                JOIN users u ON ja.freelancer_id = u.id
                JOIN freelancer_profiles fp ON ja.freelancer_profile_id = fp.id
                WHERE ja.job_id = %s
                ORDER BY ja.applied_at DESC
            """, (job_id,))
            
            applications = cursor.fetchall()
            result = []
            
            # Get skills for each applicant
            for app in applications:
                app = dict(app)
                cursor.execute("""
                    SELECT s.name
                    FROM freelancer_skills fs
                    JOIN skills s ON fs.skill_id = s.id
                    WHERE fs.freelancer_profile_id = %s
                """, (app['freelancer_profile_id'],))
                app['skills'] = [s['name'] for s in cursor.fetchall()]
                result.append(app)
            
            return result
        except Exception as e:
            print(f"❌ Error getting applications by job: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_by_freelancer(freelancer_id):
        """Get all applications by a freelancer"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
                       rp.company_name
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
                WHERE ja.freelancer_id = %s
                ORDER BY ja.applied_at DESC
            """, (freelancer_id,))
            
            applications = cursor.fetchall()
            return [dict(app) for app in applications]
        except Exception as e:
            print(f"❌ Error getting applications by freelancer: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class Notification:
    @staticmethod
    def create(user_id, title, message, notification_type='application', 
               related_application_id=None, related_job_id=None):
        """Create a new notification"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO notifications (
                    user_id, title, message, notification_type,
                    related_application_id, related_job_id
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, title, message, notification_type, 
                  related_application_id, related_job_id))
            
            notification_id = cursor.lastrowid
            connection.commit()
            print(f"✅ Notification {notification_id} created for user {user_id}")
            return notification_id
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating notification: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_by_user(user_id, unread_only=False, limit=50):
        """Get notifications for a user"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                SELECT * FROM notifications 
                WHERE user_id = %s
            """
            params = [user_id]
            
            if unread_only:
                query += " AND is_read = FALSE"
            
            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            notifications = cursor.fetchall()
            return [dict(n) for n in notifications]
        except Exception as e:
            print(f"❌ Error getting notifications: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark notification as read"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                UPDATE notifications 
                SET is_read = TRUE, read_at = NOW()
                WHERE id = %s AND user_id = %s
            """, (notification_id, user_id))
            
            affected = cursor.rowcount
            connection.commit()
            return affected > 0
        except Exception as e:
            print(f"❌ Error marking notification as read: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                UPDATE notifications 
                SET is_read = TRUE, read_at = NOW()
                WHERE user_id = %s AND is_read = FALSE
            """, (user_id,))
            
            affected = cursor.rowcount
            connection.commit()
            return affected
        except Exception as e:
            print(f"❌ Error marking all notifications as read: {str(e)}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_unread_count(user_id):
        """Get unread notifications count"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM notifications 
                WHERE user_id = %s AND is_read = FALSE
            """, (user_id,))
            
            result = cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            print(f"❌ Error getting unread count: {str(e)}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()