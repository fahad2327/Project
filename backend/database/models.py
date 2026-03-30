# # # # # # from database.db_config import get_db_connection
# # # # # # from utils.auth_utils import hash_password, check_password
# # # # # # from datetime import datetime
# # # # # # import traceback

# # # # # # class User:
# # # # # #     @staticmethod
# # # # # #     def create(username, email, password, first_name, last_name, user_type):
# # # # # #         """Create a new user"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             password_hash = hash_password(password)
            
# # # # # #             cursor.execute("""
# # # # # #                 INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
# # # # # #                 VALUES (%s, %s, %s, %s, %s, %s)
# # # # # #             """, (username, email, password_hash, first_name, last_name, user_type))
            
# # # # # #             user_id = cursor.lastrowid
            
# # # # # #             # Create profile based on user type
# # # # # #             if user_type == 'freelancer':
# # # # # #                 cursor.execute("""
# # # # # #                     INSERT INTO freelancer_profiles (user_id)
# # # # # #                     VALUES (%s)
# # # # # #                 """, (user_id,))
# # # # # #             else:
# # # # # #                 cursor.execute("""
# # # # # #                     INSERT INTO recruiter_profiles (user_id, company_name)
# # # # # #                     VALUES (%s, %s)
# # # # # #                 """, (user_id, f"{first_name} {last_name}'s Company"))
            
# # # # # #             connection.commit()
# # # # # #             print(f"✅ User created successfully with ID: {user_id}")
# # # # # #             return user_id
            
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error creating user: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             raise e
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def find_by_email(email):
# # # # # #         """Find user by email"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id, username, email, password_hash, first_name, last_name, 
# # # # # #                        user_type, is_active, is_verified, date_joined, profile_picture
# # # # # #                 FROM users WHERE email = %s
# # # # # #             """, (email,))
            
# # # # # #             user = cursor.fetchone()
# # # # # #             return user
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error finding user by email: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def find_by_id(user_id):
# # # # # #         """Find user by ID"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id, username, email, first_name, last_name, 
# # # # # #                        user_type, is_active, is_verified, date_joined, profile_picture
# # # # # #                 FROM users WHERE id = %s
# # # # # #             """, (user_id,))
            
# # # # # #             user = cursor.fetchone()
# # # # # #             return user
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error finding user by ID: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def authenticate(email, password):
# # # # # #         """Authenticate user"""
# # # # # #         try:
# # # # # #             user = User.find_by_email(email)
# # # # # #             if user and check_password(password, user['password_hash']):
# # # # # #                 # Update last login
# # # # # #                 connection = get_db_connection()
# # # # # #                 cursor = connection.cursor()
# # # # # #                 cursor.execute("""
# # # # # #                     UPDATE users SET last_login = NOW() WHERE id = %s
# # # # # #                 """, (user['id'],))
# # # # # #                 connection.commit()
# # # # # #                 cursor.close()
# # # # # #                 connection.close()
                
# # # # # #                 # Remove password hash before returning
# # # # # #                 user_dict = dict(user)
# # # # # #                 del user_dict['password_hash']
# # # # # #                 return user_dict
# # # # # #             return None
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error authenticating user: {str(e)}")
# # # # # #             return None
    
# # # # # #     @staticmethod
# # # # # #     def update_last_login(user_id):
# # # # # #         """Update user's last login timestamp"""
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
# # # # # #             cursor.execute("""
# # # # # #                 UPDATE users SET last_login = NOW() WHERE id = %s
# # # # # #             """, (user_id,))
# # # # # #             connection.commit()
# # # # # #             cursor.close()
# # # # # #             connection.close()
# # # # # #             return True
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error updating last login: {str(e)}")
# # # # # #             return False

# # # # # # class FreelancerProfile:
# # # # # #     @staticmethod
# # # # # #     def get_by_user_id(user_id):
# # # # # #         """Get freelancer profile by user ID"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # # # #                        u.profile_picture as user_profile_picture
# # # # # #                 FROM freelancer_profiles fp
# # # # # #                 JOIN users u ON fp.user_id = u.id
# # # # # #                 WHERE fp.user_id = %s
# # # # # #             """, (user_id,))
            
# # # # # #             profile = cursor.fetchone()
            
# # # # # #             if profile:
# # # # # #                 # Convert to dict if it's not already
# # # # # #                 profile = dict(profile)
                
# # # # # #                 # Get skills
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # # # #                     FROM freelancer_skills fs
# # # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # # #                 """, (profile['id'],))
# # # # # #                 profile['skills'] = [dict(skill) for skill in cursor.fetchall()]
                
# # # # # #                 # Get tech stacks
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # # # #                     FROM freelancer_tech_stacks fts
# # # # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # # # #                     WHERE fts.freelancer_profile_id = %s
# # # # # #                 """, (profile['id'],))
# # # # # #                 profile['tech_stacks'] = [dict(tech) for tech in cursor.fetchall()]
            
# # # # # #             return profile
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting freelancer profile: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def update_profile(user_id, profile_data):
# # # # # #         """Update freelancer profile"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             # Get profile ID
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # # # #             """, (user_id,))
# # # # # #             profile = cursor.fetchone()
            
# # # # # #             if not profile:
# # # # # #                 print(f"❌ Freelancer profile not found for user {user_id}")
# # # # # #                 return None
            
# # # # # #             profile_id = profile['id']
            
# # # # # #             # Update basic profile fields
# # # # # #             update_fields = []
# # # # # #             values = []
            
# # # # # #             allowed_fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # # #                              'years_of_experience', 'github_url', 'linkedin_url', 
# # # # # #                              'portfolio_url', 'is_available']
            
# # # # # #             for field in allowed_fields:
# # # # # #                 if field in profile_data:
# # # # # #                     update_fields.append(f"{field} = %s")
# # # # # #                     values.append(profile_data[field])
            
# # # # # #             if update_fields:
# # # # # #                 values.append(profile_id)
# # # # # #                 query = f"""
# # # # # #                     UPDATE freelancer_profiles 
# # # # # #                     SET {', '.join(update_fields)}
# # # # # #                     WHERE id = %s
# # # # # #                 """
# # # # # #                 cursor.execute(query, values)
            
# # # # # #             # Update skills
# # # # # #             if 'skills' in profile_data:
# # # # # #                 # Delete existing skills
# # # # # #                 cursor.execute("""
# # # # # #                     DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s
# # # # # #                 """, (profile_id,))
                
# # # # # #                 # Add new skills
# # # # # #                 for skill in profile_data['skills']:
# # # # # #                     # Check if skill exists
# # # # # #                     skill_name = skill.get('name') if isinstance(skill, dict) else skill
# # # # # #                     cursor.execute("""
# # # # # #                         SELECT id FROM skills WHERE name = %s
# # # # # #                     """, (skill_name,))
# # # # # #                     skill_record = cursor.fetchone()
                    
# # # # # #                     if skill_record:
# # # # # #                         skill_id = skill_record['id']
# # # # # #                     else:
# # # # # #                         # Create new skill
# # # # # #                         cursor.execute("""
# # # # # #                             INSERT INTO skills (name) VALUES (%s)
# # # # # #                         """, (skill_name,))
# # # # # #                         skill_id = cursor.lastrowid
                    
# # # # # #                     proficiency = skill.get('proficiency_level', 'intermediate') if isinstance(skill, dict) else 'intermediate'
                    
# # # # # #                     # Add to freelancer_skills
# # # # # #                     cursor.execute("""
# # # # # #                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
# # # # # #                         VALUES (%s, %s, %s)
# # # # # #                     """, (profile_id, skill_id, proficiency))
            
# # # # # #             # Update tech stacks
# # # # # #             if 'tech_stacks' in profile_data:
# # # # # #                 # Delete existing tech stacks
# # # # # #                 cursor.execute("""
# # # # # #                     DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s
# # # # # #                 """, (profile_id,))
                
# # # # # #                 # Add new tech stacks
# # # # # #                 for tech in profile_data['tech_stacks']:
# # # # # #                     tech_name = tech.get('name') if isinstance(tech, dict) else tech
                    
# # # # # #                     # Check if tech stack exists
# # # # # #                     cursor.execute("""
# # # # # #                         SELECT id FROM tech_stacks WHERE name = %s
# # # # # #                     """, (tech_name,))
# # # # # #                     tech_record = cursor.fetchone()
                    
# # # # # #                     if tech_record:
# # # # # #                         tech_id = tech_record['id']
# # # # # #                     else:
# # # # # #                         # Create new tech stack
# # # # # #                         cursor.execute("""
# # # # # #                             INSERT INTO tech_stacks (name) VALUES (%s)
# # # # # #                         """, (tech_name,))
# # # # # #                         tech_id = cursor.lastrowid
                    
# # # # # #                     experience = tech.get('experience_years', 0) if isinstance(tech, dict) else 0
                    
# # # # # #                     # Add to freelancer_tech_stacks
# # # # # #                     cursor.execute("""
# # # # # #                         INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
# # # # # #                         VALUES (%s, %s, %s)
# # # # # #                     """, (profile_id, tech_id, experience))
            
# # # # # #             connection.commit()
# # # # # #             print(f"✅ Freelancer profile updated for user {user_id}")
            
# # # # # #             return FreelancerProfile.get_by_user_id(user_id)
            
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error updating freelancer profile: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def search_freelancers(filters):
# # # # # #         """Search freelancers based on skills, rate, experience"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             query = """
# # # # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # # # #                        u.date_joined
# # # # # #                 FROM freelancer_profiles fp
# # # # # #                 JOIN users u ON fp.user_id = u.id
# # # # # #                 WHERE u.is_active = TRUE AND fp.is_available = TRUE
# # # # # #             """
# # # # # #             params = []
            
# # # # # #             if filters.get('min_hourly_rate'):
# # # # # #                 query += " AND fp.hourly_rate >= %s"
# # # # # #                 params.append(filters['min_hourly_rate'])
            
# # # # # #             if filters.get('max_hourly_rate'):
# # # # # #                 query += " AND fp.hourly_rate <= %s"
# # # # # #                 params.append(filters['max_hourly_rate'])
            
# # # # # #             if filters.get('years_experience_min'):
# # # # # #                 query += " AND fp.years_of_experience >= %s"
# # # # # #                 params.append(filters['years_experience_min'])
            
# # # # # #             if filters.get('skill'):
# # # # # #                 query += """ AND fp.id IN (
# # # # # #                     SELECT fs.freelancer_profile_id 
# # # # # #                     FROM freelancer_skills fs
# # # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # # #                     WHERE s.name LIKE %s
# # # # # #                 )"""
# # # # # #                 params.append(f'%{filters["skill"]}%')
            
# # # # # #             query += " ORDER BY fp.created_at DESC LIMIT 50"
            
# # # # # #             cursor.execute(query, params)
# # # # # #             freelancers = cursor.fetchall()
            
# # # # # #             # Get skills and tech stacks for each freelancer
# # # # # #             result = []
# # # # # #             for freelancer in freelancers:
# # # # # #                 freelancer = dict(freelancer)
                
# # # # # #                 # Get skills
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # # # #                     FROM freelancer_skills fs
# # # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # # #                 """, (freelancer['id'],))
# # # # # #                 freelancer['skills'] = [dict(skill) for skill in cursor.fetchall()]
                
# # # # # #                 # Get tech stacks
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # # # #                     FROM freelancer_tech_stacks fts
# # # # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # # # #                     WHERE fts.freelancer_profile_id = %s
# # # # # #                 """, (freelancer['id'],))
# # # # # #                 freelancer['tech_stacks'] = [dict(tech) for tech in cursor.fetchall()]
                
# # # # # #                 result.append(freelancer)
            
# # # # # #             return result
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error searching freelancers: {str(e)}")
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()

# # # # # # class RecruiterProfile:
# # # # # #     @staticmethod
# # # # # #     def get_by_user_id(user_id):
# # # # # #         """Get recruiter profile by user ID"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT rp.*, u.username, u.email, u.first_name, u.last_name
# # # # # #                 FROM recruiter_profiles rp
# # # # # #                 JOIN users u ON rp.user_id = u.id
# # # # # #                 WHERE rp.user_id = %s
# # # # # #             """, (user_id,))
            
# # # # # #             profile = cursor.fetchone()
# # # # # #             if profile:
# # # # # #                 profile = dict(profile)
# # # # # #             return profile
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting recruiter profile: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def update_profile(user_id, profile_data):
# # # # # #         """Update recruiter profile"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             update_fields = []
# # # # # #             values = []
            
# # # # # #             allowed_fields = ['company_name', 'company_website', 'company_size', 
# # # # # #                              'industry', 'company_description', 'location', 'phone']
            
# # # # # #             for field in allowed_fields:
# # # # # #                 if field in profile_data:
# # # # # #                     update_fields.append(f"{field} = %s")
# # # # # #                     values.append(profile_data[field])
            
# # # # # #             if update_fields:
# # # # # #                 values.append(user_id)
# # # # # #                 query = f"""
# # # # # #                     UPDATE recruiter_profiles 
# # # # # #                     SET {', '.join(update_fields)}
# # # # # #                     WHERE user_id = %s
# # # # # #                 """
# # # # # #                 cursor.execute(query, values)
# # # # # #                 connection.commit()
# # # # # #                 print(f"✅ Recruiter profile updated for user {user_id}")
            
# # # # # #             return RecruiterProfile.get_by_user_id(user_id)
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error updating recruiter profile: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()

# # # # # # class Job:
# # # # # #     @staticmethod
# # # # # #     def create(recruiter_id, job_data):
# # # # # #         """Create a new job posting"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             # Get recruiter profile ID
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id FROM recruiter_profiles WHERE user_id = %s
# # # # # #             """, (recruiter_id,))
# # # # # #             profile = cursor.fetchone()
            
# # # # # #             if not profile:
# # # # # #                 print(f"❌ Recruiter profile not found for user {recruiter_id}")
# # # # # #                 return None
            
# # # # # #             # Insert job
# # # # # #             cursor.execute("""
# # # # # #                 INSERT INTO jobs (
# # # # # #                     recruiter_id, recruiter_profile_id, title, description,
# # # # # #                     pay_per_hour, experience_level, job_type, location,
# # # # # #                     is_remote, requirements, responsibilities, benefits,
# # # # # #                     application_deadline
# # # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# # # # # #             """, (
# # # # # #                 recruiter_id, profile['id'], job_data['title'],
# # # # # #                 job_data['description'], job_data['pay_per_hour'],
# # # # # #                 job_data['experience_level'], job_data.get('job_type', 'freelance'),
# # # # # #                 job_data.get('location'), job_data.get('is_remote', True),
# # # # # #                 job_data.get('requirements'), job_data.get('responsibilities'),
# # # # # #                 job_data.get('benefits'), job_data.get('application_deadline')
# # # # # #             ))
            
# # # # # #             job_id = cursor.lastrowid
# # # # # #             print(f"✅ Job created with ID: {job_id}")
            
# # # # # #             # Add required skills
# # # # # #             if 'required_skills' in job_data and job_data['required_skills']:
# # # # # #                 for skill_name in job_data['required_skills']:
# # # # # #                     # Get or create skill
# # # # # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # # # # #                     skill = cursor.fetchone()
# # # # # #                     if skill:
# # # # # #                         skill_id = skill['id']
# # # # # #                     else:
# # # # # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # # # # #                         skill_id = cursor.lastrowid
                    
# # # # # #                     cursor.execute("""
# # # # # #                         INSERT INTO job_skills (job_id, skill_id, is_required)
# # # # # #                         VALUES (%s, %s, TRUE)
# # # # # #                     """, (job_id, skill_id))
# # # # # #                     print(f"  Added skill: {skill_name}")
            
# # # # # #             # Add tech stack
# # # # # #             if 'tech_stack' in job_data and job_data['tech_stack']:
# # # # # #                 for tech_name in job_data['tech_stack']:
# # # # # #                     # Get or create tech stack
# # # # # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # # # # #                     tech = cursor.fetchone()
# # # # # #                     if tech:
# # # # # #                         tech_id = tech['id']
# # # # # #                     else:
# # # # # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # # # # #                         tech_id = cursor.lastrowid
                    
# # # # # #                     cursor.execute("""
# # # # # #                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
# # # # # #                         VALUES (%s, %s, TRUE)
# # # # # #                     """, (job_id, tech_id))
# # # # # #                     print(f"  Added tech: {tech_name}")
            
# # # # # #             connection.commit()
# # # # # #             return job_id
            
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error creating job: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             raise e
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_by_id(job_id):
# # # # # #         """Get job by ID"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT j.*, rp.company_name, u.email as recruiter_email,
# # # # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # # # #                 FROM jobs j
# # # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # # #                 JOIN users u ON j.recruiter_id = u.id
# # # # # #                 WHERE j.id = %s
# # # # # #             """, (job_id,))
            
# # # # # #             job = cursor.fetchone()
            
# # # # # #             if job:
# # # # # #                 job = dict(job)
                
# # # # # #                 # Get required skills
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT s.id, s.name
# # # # # #                     FROM job_skills js
# # # # # #                     JOIN skills s ON js.skill_id = s.id
# # # # # #                     WHERE js.job_id = %s AND js.is_required = TRUE
# # # # # #                 """, (job_id,))
# # # # # #                 job['required_skills'] = [s['name'] for s in cursor.fetchall()]
                
# # # # # #                 # Get tech stack
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT ts.id, ts.name
# # # # # #                     FROM job_tech_stacks jts
# # # # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # # # #                     WHERE jts.job_id = %s AND jts.is_required = TRUE
# # # # # #                 """, (job_id,))
# # # # # #                 job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
                
# # # # # #                 # Increment view count
# # # # # #                 cursor.execute("""
# # # # # #                     UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
# # # # # #                 """, (job_id,))
# # # # # #                 connection.commit()
# # # # # #                 print(f"👁️ Job {job_id} view count incremented")
            
# # # # # #             return job
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting job by ID: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def search_jobs(filters):
# # # # # #         """Search jobs with filters"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             query = """
# # # # # #                 SELECT j.*, rp.company_name,
# # # # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # # # #                 FROM jobs j
# # # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # # #                 JOIN users u ON j.recruiter_id = u.id
# # # # # #                 WHERE j.is_active = TRUE
# # # # # #             """
# # # # # #             params = []
            
# # # # # #             # IMPROVED SEARCH: Case-insensitive search with better matching
# # # # # #             if filters.get('search'):
# # # # # #                 search_term = f'%{filters["search"]}%'
# # # # # #                 query += """ AND (
# # # # # #                     LOWER(j.title) LIKE LOWER(%s) OR 
# # # # # #                     LOWER(j.description) LIKE LOWER(%s) OR 
# # # # # #                     LOWER(j.requirements) LIKE LOWER(%s) OR
# # # # # #                     LOWER(j.title) LIKE LOWER(%s)
# # # # # #                 )"""
# # # # # #                 params.extend([search_term, search_term, search_term, search_term])
# # # # # #                 print(f"🔍 Searching with term: {filters['search']}")
            
# # # # # #             if filters.get('experience_level'):
# # # # # #                 query += " AND j.experience_level = %s"
# # # # # #                 params.append(filters['experience_level'])
            
# # # # # #             if filters.get('min_pay'):
# # # # # #                 try:
# # # # # #                     min_pay = float(filters['min_pay'])
# # # # # #                     query += " AND j.pay_per_hour >= %s"
# # # # # #                     params.append(min_pay)
# # # # # #                 except (ValueError, TypeError):
# # # # # #                     pass
            
# # # # # #             if filters.get('max_pay'):
# # # # # #                 try:
# # # # # #                     max_pay = float(filters['max_pay'])
# # # # # #                     query += " AND j.pay_per_hour <= %s"
# # # # # #                     params.append(max_pay)
# # # # # #                 except (ValueError, TypeError):
# # # # # #                     pass
            
# # # # # #             if filters.get('job_type'):
# # # # # #                 query += " AND j.job_type = %s"
# # # # # #                 params.append(filters['job_type'])
            
# # # # # #             if filters.get('is_remote'):
# # # # # #                 query += " AND j.is_remote = TRUE"
            
# # # # # #             query += " ORDER BY j.created_at DESC"
            
# # # # # #             print(f"📝 Executing query: {query}")
# # # # # #             print(f"📝 With params: {params}")
            
# # # # # #             cursor.execute(query, params)
# # # # # #             jobs = cursor.fetchall()
            
# # # # # #             print(f"✅ Found {len(jobs)} jobs")
            
# # # # # #             # Get skills and tech stack for each job
# # # # # #             result = []
# # # # # #             for job in jobs:
# # # # # #                 job = dict(job)
                
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT s.name
# # # # # #                     FROM job_skills js
# # # # # #                     JOIN skills s ON js.skill_id = s.id
# # # # # #                     WHERE js.job_id = %s
# # # # # #                 """, (job['id'],))
# # # # # #                 job['required_skills'] = [s['name'] for s in cursor.fetchall()]
                
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT ts.name
# # # # # #                     FROM job_tech_stacks jts
# # # # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # # # #                     WHERE jts.job_id = %s
# # # # # #                 """, (job['id'],))
# # # # # #                 job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
                
# # # # # #                 result.append(job)
            
# # # # # #             return result
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error searching jobs: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_by_recruiter(recruiter_id):
# # # # # #         """Get all jobs posted by a recruiter"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT j.*, 
# # # # # #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as total_applications
# # # # # #                 FROM jobs j
# # # # # #                 WHERE j.recruiter_id = %s
# # # # # #                 ORDER BY j.created_at DESC
# # # # # #             """, (recruiter_id,))
            
# # # # # #             jobs = cursor.fetchall()
# # # # # #             result = [dict(job) for job in jobs]
# # # # # #             return result
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting jobs by recruiter: {str(e)}")
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()

# # # # # # class JobApplication:
# # # # # #     @staticmethod
# # # # # #     def create(job_id, freelancer_id, application_data):
# # # # # #         """Create a new job application"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             # Check if already applied
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id FROM job_applications 
# # # # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # # # #             """, (job_id, freelancer_id))
            
# # # # # #             if cursor.fetchone():
# # # # # #                 print(f"⚠️ Freelancer {freelancer_id} already applied to job {job_id}")
# # # # # #                 return None
            
# # # # # #             # Get freelancer profile ID
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # # # #             """, (freelancer_id,))
# # # # # #             profile = cursor.fetchone()
            
# # # # # #             if not profile:
# # # # # #                 print(f"❌ Freelancer profile not found for user {freelancer_id}")
# # # # # #                 return None
            
# # # # # #             # Create application
# # # # # #             cursor.execute("""
# # # # # #                 INSERT INTO job_applications (
# # # # # #                     job_id, freelancer_id, freelancer_profile_id,
# # # # # #                     cover_letter, proposed_rate, availability_date
# # # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s)
# # # # # #             """, (
# # # # # #                 job_id, freelancer_id, profile['id'],
# # # # # #                 application_data.get('cover_letter'),
# # # # # #                 application_data.get('proposed_rate'),
# # # # # #                 application_data.get('availability_date')
# # # # # #             ))
            
# # # # # #             application_id = cursor.lastrowid
            
# # # # # #             # Update job applications count
# # # # # #             cursor.execute("""
# # # # # #                 UPDATE jobs SET applications_count = applications_count + 1
# # # # # #                 WHERE id = %s
# # # # # #             """, (job_id,))
            
# # # # # #             connection.commit()
# # # # # #             print(f"✅ Application {application_id} created for job {job_id}")
# # # # # #             return application_id
            
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error creating application: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def update_status(application_id, status, recruiter_notes=None):
# # # # # #         """Update application status"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             # Get application details
# # # # # #             cursor.execute("""
# # # # # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # # # # #                        u.email as freelancer_email,
# # # # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # # # # #                 FROM job_applications ja
# # # # # #                 JOIN jobs j ON ja.job_id = j.id
# # # # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # # # #                 WHERE ja.id = %s
# # # # # #             """, (application_id,))
            
# # # # # #             application = cursor.fetchone()
            
# # # # # #             if not application:
# # # # # #                 print(f"❌ Application {application_id} not found")
# # # # # #                 return None
            
# # # # # #             # Update status with timestamp
# # # # # #             timestamp_field = {
# # # # # #                 'reviewed': 'reviewed_at',
# # # # # #                 'accepted': 'accepted_at',
# # # # # #                 'rejected': 'rejected_at'
# # # # # #             }.get(status)
            
# # # # # #             if timestamp_field:
# # # # # #                 cursor.execute(f"""
# # # # # #                     UPDATE job_applications 
# # # # # #                     SET status = %s, recruiter_notes = %s, {timestamp_field} = NOW()
# # # # # #                     WHERE id = %s
# # # # # #                 """, (status, recruiter_notes, application_id))
# # # # # #             else:
# # # # # #                 cursor.execute("""
# # # # # #                     UPDATE job_applications 
# # # # # #                     SET status = %s, recruiter_notes = %s
# # # # # #                     WHERE id = %s
# # # # # #                 """, (status, recruiter_notes, application_id))
            
# # # # # #             connection.commit()
# # # # # #             print(f"✅ Application {application_id} status updated to {status}")
# # # # # #             return dict(application)
            
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error updating application status: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_by_job(job_id):
# # # # # #         """Get all applications for a job"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT ja.*, 
# # # # # #                        fp.hourly_rate, fp.years_of_experience,
# # # # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
# # # # # #                        u.email as freelancer_email
# # # # # #                 FROM job_applications ja
# # # # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # # # #                 JOIN freelancer_profiles fp ON ja.freelancer_profile_id = fp.id
# # # # # #                 WHERE ja.job_id = %s
# # # # # #                 ORDER BY ja.applied_at DESC
# # # # # #             """, (job_id,))
            
# # # # # #             applications = cursor.fetchall()
# # # # # #             result = []
            
# # # # # #             # Get skills for each applicant
# # # # # #             for app in applications:
# # # # # #                 app = dict(app)
# # # # # #                 cursor.execute("""
# # # # # #                     SELECT s.name
# # # # # #                     FROM freelancer_skills fs
# # # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # # #                 """, (app['freelancer_profile_id'],))
# # # # # #                 app['skills'] = [s['name'] for s in cursor.fetchall()]
# # # # # #                 result.append(app)
            
# # # # # #             return result
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting applications by job: {str(e)}")
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_by_freelancer(freelancer_id):
# # # # # #         """Get all applications by a freelancer"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
# # # # # #                        rp.company_name
# # # # # #                 FROM job_applications ja
# # # # # #                 JOIN jobs j ON ja.job_id = j.id
# # # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # # #                 WHERE ja.freelancer_id = %s
# # # # # #                 ORDER BY ja.applied_at DESC
# # # # # #             """, (freelancer_id,))
            
# # # # # #             applications = cursor.fetchall()
# # # # # #             return [dict(app) for app in applications]
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting applications by freelancer: {str(e)}")
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()

# # # # # # class Notification:
# # # # # #     @staticmethod
# # # # # #     def create(user_id, title, message, notification_type='application', 
# # # # # #                related_application_id=None, related_job_id=None):
# # # # # #         """Create a new notification"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 INSERT INTO notifications (
# # # # # #                     user_id, title, message, notification_type,
# # # # # #                     related_application_id, related_job_id
# # # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s)
# # # # # #             """, (user_id, title, message, notification_type, 
# # # # # #                   related_application_id, related_job_id))
            
# # # # # #             notification_id = cursor.lastrowid
# # # # # #             connection.commit()
# # # # # #             print(f"✅ Notification {notification_id} created for user {user_id}")
# # # # # #             return notification_id
# # # # # #         except Exception as e:
# # # # # #             if connection:
# # # # # #                 connection.rollback()
# # # # # #             print(f"❌ Error creating notification: {str(e)}")
# # # # # #             return None
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_by_user(user_id, unread_only=False, limit=50):
# # # # # #         """Get notifications for a user"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             query = """
# # # # # #                 SELECT * FROM notifications 
# # # # # #                 WHERE user_id = %s
# # # # # #             """
# # # # # #             params = [user_id]
            
# # # # # #             if unread_only:
# # # # # #                 query += " AND is_read = FALSE"
            
# # # # # #             query += " ORDER BY created_at DESC LIMIT %s"
# # # # # #             params.append(limit)
            
# # # # # #             cursor.execute(query, params)
# # # # # #             notifications = cursor.fetchall()
# # # # # #             return [dict(n) for n in notifications]
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting notifications: {str(e)}")
# # # # # #             return []
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def mark_as_read(notification_id, user_id):
# # # # # #         """Mark notification as read"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 UPDATE notifications 
# # # # # #                 SET is_read = TRUE, read_at = NOW()
# # # # # #                 WHERE id = %s AND user_id = %s
# # # # # #             """, (notification_id, user_id))
            
# # # # # #             affected = cursor.rowcount
# # # # # #             connection.commit()
# # # # # #             return affected > 0
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error marking notification as read: {str(e)}")
# # # # # #             return False
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def mark_all_as_read(user_id):
# # # # # #         """Mark all notifications as read for a user"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 UPDATE notifications 
# # # # # #                 SET is_read = TRUE, read_at = NOW()
# # # # # #                 WHERE user_id = %s AND is_read = FALSE
# # # # # #             """, (user_id,))
            
# # # # # #             affected = cursor.rowcount
# # # # # #             connection.commit()
# # # # # #             return affected
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error marking all notifications as read: {str(e)}")
# # # # # #             return 0
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()
    
# # # # # #     @staticmethod
# # # # # #     def get_unread_count(user_id):
# # # # # #         """Get unread notifications count"""
# # # # # #         connection = None
# # # # # #         cursor = None
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
            
# # # # # #             cursor.execute("""
# # # # # #                 SELECT COUNT(*) as count
# # # # # #                 FROM notifications 
# # # # # #                 WHERE user_id = %s AND is_read = FALSE
# # # # # #             """, (user_id,))
            
# # # # # #             result = cursor.fetchone()
# # # # # #             return result['count'] if result else 0
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error getting unread count: {str(e)}")
# # # # # #             return 0
# # # # # #         finally:
# # # # # #             if cursor:
# # # # # #                 cursor.close()
# # # # # #             if connection:
# # # # # #                 connection.close()








# # # # # # database/models.py

# # # # # from database.db_config import get_db_connection
# # # # # from utils.auth_utils import hash_password, check_password
# # # # # from datetime import datetime
# # # # # import traceback
# # # # # import mysql.connector

# # # # # class User:
# # # # #     @staticmethod
# # # # #     def create(username, email, password, first_name, last_name, user_type):
# # # # #         """Create a new user"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             password_hash = hash_password(password)
            
# # # # #             # Insert user with verification fields
# # # # #             cursor.execute("""
# # # # #                 INSERT INTO users (
# # # # #                     username, email, password_hash, first_name, last_name, 
# # # # #                     user_type, is_verified, created_at
# # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
# # # # #             """, (
# # # # #                 username, email, password_hash, first_name, last_name, 
# # # # #                 user_type, False
# # # # #             ))
            
# # # # #             user_id = cursor.lastrowid
            
# # # # #             # Create profile based on user type
# # # # #             if user_type == 'freelancer':
# # # # #                 cursor.execute("""
# # # # #                     INSERT INTO freelancer_profiles (user_id, is_available)
# # # # #                     VALUES (%s, %s)
# # # # #                 """, (user_id, True))
# # # # #             else:
# # # # #                 cursor.execute("""
# # # # #                     INSERT INTO recruiter_profiles (user_id, company_name)
# # # # #                     VALUES (%s, %s)
# # # # #                 """, (user_id, f"{first_name} {last_name}'s Company"))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ User created successfully with ID: {user_id}")
# # # # #             return user_id
            
# # # # #         except mysql.connector.Error as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Database error creating user: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             raise e
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error creating user: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             raise e
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def find_by_email(email):
# # # # #         """Find user by email"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT id, username, email, password_hash, first_name, last_name, 
# # # # #                        user_type, is_verified, created_at
# # # # #                 FROM users WHERE email = %s
# # # # #             """, (email,))
            
# # # # #             user = cursor.fetchone()
# # # # #             return user
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error finding user by email: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def find_by_id(user_id):
# # # # #         """Find user by ID"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT id, username, email, first_name, last_name, 
# # # # #                        user_type, is_verified, created_at
# # # # #                 FROM users WHERE id = %s
# # # # #             """, (user_id,))
            
# # # # #             user = cursor.fetchone()
# # # # #             return user
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error finding user by ID: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def find_by_verification_token(token):
# # # # #         """Find user by verification token"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT id, username, email, first_name, last_name, 
# # # # #                        user_type, is_verified
# # # # #                 FROM users 
# # # # #                 WHERE email_verification_token = %s 
# # # # #                 AND verification_sent_at > DATE_SUB(NOW(), INTERVAL 24 HOUR)
# # # # #             """, (token,))
            
# # # # #             user = cursor.fetchone()
# # # # #             return user
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error finding user by token: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def authenticate(email, password):
# # # # #         """Authenticate user"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             user = User.find_by_email(email)
# # # # #             if user and check_password(password, user['password_hash']):
# # # # #                 # Update last login
# # # # #                 connection = get_db_connection()
# # # # #                 cursor = connection.cursor()
# # # # #                 cursor.execute("""
# # # # #                     UPDATE users SET last_login = NOW() WHERE id = %s
# # # # #                 """, (user['id'],))
# # # # #                 connection.commit()
                
# # # # #                 # Remove password hash before returning
# # # # #                 user.pop('password_hash', None)
# # # # #                 return user
# # # # #             return None
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error authenticating user: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def set_verification_token(user_id, token):
# # # # #         """Set email verification token"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             cursor.execute("""
# # # # #                 UPDATE users 
# # # # #                 SET email_verification_token = %s, verification_sent_at = NOW()
# # # # #                 WHERE id = %s
# # # # #             """, (token, user_id))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ Verification token set for user {user_id}")
# # # # #             return True
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error setting verification token: {str(e)}")
# # # # #             return False
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def verify_email(user_id):
# # # # #         """Mark user email as verified"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             cursor.execute("""
# # # # #                 UPDATE users 
# # # # #                 SET is_verified = TRUE, verified_at = NOW(), 
# # # # #                     email_verification_token = NULL
# # # # #                 WHERE id = %s
# # # # #             """, (user_id,))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ Email verified for user {user_id}")
# # # # #             return True
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error verifying email: {str(e)}")
# # # # #             return False
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def update_last_login(user_id):
# # # # #         """Update user's last login timestamp"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
# # # # #             cursor.execute("""
# # # # #                 UPDATE users SET last_login = NOW() WHERE id = %s
# # # # #             """, (user_id,))
# # # # #             connection.commit()
# # # # #             return True
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error updating last login: {str(e)}")
# # # # #             return False
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()


# # # # # class FreelancerProfile:
# # # # #     @staticmethod
# # # # #     def get_by_user_id(user_id):
# # # # #         """Get freelancer profile by user ID"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # # #                        u.profile_picture, u.is_verified
# # # # #                 FROM freelancer_profiles fp
# # # # #                 JOIN users u ON fp.user_id = u.id
# # # # #                 WHERE fp.user_id = %s
# # # # #             """, (user_id,))
            
# # # # #             profile = cursor.fetchone()
            
# # # # #             if profile:
# # # # #                 # Get skills
# # # # #                 cursor.execute("""
# # # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # # #                     FROM freelancer_skills fs
# # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # #                 """, (profile['id'],))
# # # # #                 profile['skills'] = cursor.fetchall()
                
# # # # #                 # Get tech stacks
# # # # #                 cursor.execute("""
# # # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # # #                     FROM freelancer_tech_stacks fts
# # # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # # #                     WHERE fts.freelancer_profile_id = %s
# # # # #                 """, (profile['id'],))
# # # # #                 profile['tech_stacks'] = cursor.fetchall()
            
# # # # #             return profile
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting freelancer profile: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def update_profile(user_id, profile_data):
# # # # #         """Update freelancer profile"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             # Get profile ID
# # # # #             cursor.execute("""
# # # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # # #             """, (user_id,))
# # # # #             profile = cursor.fetchone()
            
# # # # #             if not profile:
# # # # #                 print(f"❌ Freelancer profile not found for user {user_id}")
# # # # #                 return None
            
# # # # #             profile_id = profile['id']
            
# # # # #             # Update basic profile fields
# # # # #             update_fields = []
# # # # #             values = []
            
# # # # #             allowed_fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # #                              'years_of_experience', 'github_url', 'linkedin_url', 
# # # # #                              'portfolio_url', 'is_available']
            
# # # # #             for field in allowed_fields:
# # # # #                 if field in profile_data:
# # # # #                     update_fields.append(f"{field} = %s")
# # # # #                     values.append(profile_data[field])
            
# # # # #             if update_fields:
# # # # #                 values.append(profile_id)
# # # # #                 query = f"""
# # # # #                     UPDATE freelancer_profiles 
# # # # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # # # #                     WHERE id = %s
# # # # #                 """
# # # # #                 cursor.execute(query, values)
            
# # # # #             # Update skills
# # # # #             if 'skills' in profile_data:
# # # # #                 # Delete existing skills
# # # # #                 cursor.execute("""
# # # # #                     DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s
# # # # #                 """, (profile_id,))
                
# # # # #                 # Add new skills
# # # # #                 for skill in profile_data['skills']:
# # # # #                     skill_name = skill.get('name') if isinstance(skill, dict) else skill
                    
# # # # #                     # Get or create skill
# # # # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # # # #                     skill_record = cursor.fetchone()
                    
# # # # #                     if skill_record:
# # # # #                         skill_id = skill_record['id']
# # # # #                     else:
# # # # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # # # #                         skill_id = cursor.lastrowid
                    
# # # # #                     proficiency = skill.get('proficiency_level', 'intermediate') if isinstance(skill, dict) else 'intermediate'
                    
# # # # #                     cursor.execute("""
# # # # #                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
# # # # #                         VALUES (%s, %s, %s)
# # # # #                     """, (profile_id, skill_id, proficiency))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ Freelancer profile updated for user {user_id}")
            
# # # # #             return FreelancerProfile.get_by_user_id(user_id)
            
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error updating freelancer profile: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def search_freelancers(filters):
# # # # #         """Search freelancers based on skills, rate, experience"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             query = """
# # # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # # #                        u.created_at
# # # # #                 FROM freelancer_profiles fp
# # # # #                 JOIN users u ON fp.user_id = u.id
# # # # #                 WHERE u.is_active = TRUE AND fp.is_available = TRUE
# # # # #             """
# # # # #             params = []
            
# # # # #             if filters.get('min_hourly_rate'):
# # # # #                 query += " AND fp.hourly_rate >= %s"
# # # # #                 params.append(filters['min_hourly_rate'])
            
# # # # #             if filters.get('max_hourly_rate'):
# # # # #                 query += " AND fp.hourly_rate <= %s"
# # # # #                 params.append(filters['max_hourly_rate'])
            
# # # # #             if filters.get('years_experience_min'):
# # # # #                 query += " AND fp.years_of_experience >= %s"
# # # # #                 params.append(filters['years_experience_min'])
            
# # # # #             if filters.get('skill'):
# # # # #                 query += """ AND fp.id IN (
# # # # #                     SELECT fs.freelancer_profile_id 
# # # # #                     FROM freelancer_skills fs
# # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # #                     WHERE s.name LIKE %s
# # # # #                 )"""
# # # # #                 params.append(f'%{filters["skill"]}%')
            
# # # # #             query += " ORDER BY fp.created_at DESC LIMIT 50"
            
# # # # #             cursor.execute(query, params)
# # # # #             freelancers = cursor.fetchall()
            
# # # # #             # Get skills and tech stacks for each freelancer
# # # # #             result = []
# # # # #             for freelancer in freelancers:
# # # # #                 # Get skills
# # # # #                 cursor.execute("""
# # # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # # #                     FROM freelancer_skills fs
# # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # #                 """, (freelancer['id'],))
# # # # #                 freelancer['skills'] = cursor.fetchall()
                
# # # # #                 # Get tech stacks
# # # # #                 cursor.execute("""
# # # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # # #                     FROM freelancer_tech_stacks fts
# # # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # # #                     WHERE fts.freelancer_profile_id = %s
# # # # #                 """, (freelancer['id'],))
# # # # #                 freelancer['tech_stacks'] = cursor.fetchall()
                
# # # # #                 result.append(freelancer)
            
# # # # #             return result
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error searching freelancers: {str(e)}")
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()


# # # # # class RecruiterProfile:
# # # # #     @staticmethod
# # # # #     def get_by_user_id(user_id):
# # # # #         """Get recruiter profile by user ID"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT rp.*, u.username, u.email, u.first_name, u.last_name
# # # # #                 FROM recruiter_profiles rp
# # # # #                 JOIN users u ON rp.user_id = u.id
# # # # #                 WHERE rp.user_id = %s
# # # # #             """, (user_id,))
            
# # # # #             profile = cursor.fetchone()
# # # # #             return profile
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting recruiter profile: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def update_profile(user_id, profile_data):
# # # # #         """Update recruiter profile"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             update_fields = []
# # # # #             values = []
            
# # # # #             allowed_fields = ['company_name', 'company_website', 'company_size', 
# # # # #                              'industry', 'company_description', 'location', 'phone']
            
# # # # #             for field in allowed_fields:
# # # # #                 if field in profile_data:
# # # # #                     update_fields.append(f"{field} = %s")
# # # # #                     values.append(profile_data[field])
            
# # # # #             if update_fields:
# # # # #                 values.append(user_id)
# # # # #                 query = f"""
# # # # #                     UPDATE recruiter_profiles 
# # # # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # # # #                     WHERE user_id = %s
# # # # #                 """
# # # # #                 cursor.execute(query, values)
# # # # #                 connection.commit()
# # # # #                 print(f"✅ Recruiter profile updated for user {user_id}")
            
# # # # #             return RecruiterProfile.get_by_user_id(user_id)
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error updating recruiter profile: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()


# # # # # class Job:
# # # # #     @staticmethod
# # # # #     def create(recruiter_id, job_data):
# # # # #         """Create a new job posting"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             # Get recruiter profile ID
# # # # #             cursor.execute("""
# # # # #                 SELECT id FROM recruiter_profiles WHERE user_id = %s
# # # # #             """, (recruiter_id,))
# # # # #             profile = cursor.fetchone()
            
# # # # #             if not profile:
# # # # #                 print(f"❌ Recruiter profile not found for user {recruiter_id}")
# # # # #                 return None
            
# # # # #             # Insert job
# # # # #             cursor.execute("""
# # # # #                 INSERT INTO jobs (
# # # # #                     recruiter_id, recruiter_profile_id, title, description,
# # # # #                     pay_per_hour, experience_level, job_type, location,
# # # # #                     is_remote, requirements, responsibilities, benefits,
# # # # #                     application_deadline, created_at
# # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
# # # # #             """, (
# # # # #                 recruiter_id, profile['id'], job_data['title'],
# # # # #                 job_data['description'], job_data['pay_per_hour'],
# # # # #                 job_data['experience_level'], job_data.get('job_type', 'freelance'),
# # # # #                 job_data.get('location'), job_data.get('is_remote', True),
# # # # #                 job_data.get('requirements'), job_data.get('responsibilities'),
# # # # #                 job_data.get('benefits'), job_data.get('application_deadline')
# # # # #             ))
            
# # # # #             job_id = cursor.lastrowid
# # # # #             print(f"✅ Job created with ID: {job_id}")
            
# # # # #             # Add required skills
# # # # #             if 'required_skills' in job_data and job_data['required_skills']:
# # # # #                 for skill_name in job_data['required_skills']:
# # # # #                     # Get or create skill
# # # # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # # # #                     skill = cursor.fetchone()
# # # # #                     if skill:
# # # # #                         skill_id = skill['id']
# # # # #                     else:
# # # # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # # # #                         skill_id = cursor.lastrowid
                    
# # # # #                     cursor.execute("""
# # # # #                         INSERT INTO job_skills (job_id, skill_id, is_required)
# # # # #                         VALUES (%s, %s, TRUE)
# # # # #                     """, (job_id, skill_id))
            
# # # # #             # Add tech stack
# # # # #             if 'tech_stack' in job_data and job_data['tech_stack']:
# # # # #                 for tech_name in job_data['tech_stack']:
# # # # #                     # Get or create tech stack
# # # # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # # # #                     tech = cursor.fetchone()
# # # # #                     if tech:
# # # # #                         tech_id = tech['id']
# # # # #                     else:
# # # # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # # # #                         tech_id = cursor.lastrowid
                    
# # # # #                     cursor.execute("""
# # # # #                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
# # # # #                         VALUES (%s, %s, TRUE)
# # # # #                     """, (job_id, tech_id))
            
# # # # #             connection.commit()
# # # # #             return job_id
            
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error creating job: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_by_id(job_id):
# # # # #         """Get job by ID"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT j.*, rp.company_name, u.email as recruiter_email,
# # # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # # #                 FROM jobs j
# # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # #                 JOIN users u ON j.recruiter_id = u.id
# # # # #                 WHERE j.id = %s
# # # # #             """, (job_id,))
            
# # # # #             job = cursor.fetchone()
            
# # # # #             if job:
# # # # #                 # Get required skills
# # # # #                 cursor.execute("""
# # # # #                     SELECT s.id, s.name
# # # # #                     FROM job_skills js
# # # # #                     JOIN skills s ON js.skill_id = s.id
# # # # #                     WHERE js.job_id = %s AND js.is_required = TRUE
# # # # #                 """, (job_id,))
# # # # #                 job['required_skills'] = [skill['name'] for skill in cursor.fetchall()]
                
# # # # #                 # Get tech stack
# # # # #                 cursor.execute("""
# # # # #                     SELECT ts.id, ts.name
# # # # #                     FROM job_tech_stacks jts
# # # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # # #                     WHERE jts.job_id = %s AND jts.is_required = TRUE
# # # # #                 """, (job_id,))
# # # # #                 job['tech_stack'] = [tech['name'] for tech in cursor.fetchall()]
                
# # # # #                 # Increment view count
# # # # #                 cursor.execute("""
# # # # #                     UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
# # # # #                 """, (job_id,))
# # # # #                 connection.commit()
            
# # # # #             return job
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting job by ID: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def search_jobs(filters):
# # # # #         """Search jobs with filters"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             query = """
# # # # #                 SELECT j.*, rp.company_name,
# # # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # # #                 FROM jobs j
# # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # #                 JOIN users u ON j.recruiter_id = u.id
# # # # #                 WHERE j.is_active = TRUE
# # # # #             """
# # # # #             params = []
            
# # # # #             if filters.get('search'):
# # # # #                 search_term = f'%{filters["search"]}%'
# # # # #                 query += """ AND (
# # # # #                     LOWER(j.title) LIKE LOWER(%s) OR 
# # # # #                     LOWER(j.description) LIKE LOWER(%s) OR 
# # # # #                     LOWER(j.requirements) LIKE LOWER(%s)
# # # # #                 )"""
# # # # #                 params.extend([search_term, search_term, search_term])
            
# # # # #             if filters.get('experience_level'):
# # # # #                 query += " AND j.experience_level = %s"
# # # # #                 params.append(filters['experience_level'])
            
# # # # #             if filters.get('min_pay'):
# # # # #                 try:
# # # # #                     min_pay = float(filters['min_pay'])
# # # # #                     query += " AND j.pay_per_hour >= %s"
# # # # #                     params.append(min_pay)
# # # # #                 except (ValueError, TypeError):
# # # # #                     pass
            
# # # # #             if filters.get('max_pay'):
# # # # #                 try:
# # # # #                     max_pay = float(filters['max_pay'])
# # # # #                     query += " AND j.pay_per_hour <= %s"
# # # # #                     params.append(max_pay)
# # # # #                 except (ValueError, TypeError):
# # # # #                     pass
            
# # # # #             if filters.get('job_type'):
# # # # #                 query += " AND j.job_type = %s"
# # # # #                 params.append(filters['job_type'])
            
# # # # #             if filters.get('is_remote'):
# # # # #                 query += " AND j.is_remote = TRUE"
            
# # # # #             query += " ORDER BY j.created_at DESC"
            
# # # # #             cursor.execute(query, params)
# # # # #             jobs = cursor.fetchall()
            
# # # # #             # Get skills and tech stack for each job
# # # # #             result = []
# # # # #             for job in jobs:
# # # # #                 cursor.execute("""
# # # # #                     SELECT s.name
# # # # #                     FROM job_skills js
# # # # #                     JOIN skills s ON js.skill_id = s.id
# # # # #                     WHERE js.job_id = %s
# # # # #                 """, (job['id'],))
# # # # #                 job['required_skills'] = [s['name'] for s in cursor.fetchall()]
                
# # # # #                 cursor.execute("""
# # # # #                     SELECT ts.name
# # # # #                     FROM job_tech_stacks jts
# # # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # # #                     WHERE jts.job_id = %s
# # # # #                 """, (job['id'],))
# # # # #                 job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
                
# # # # #                 result.append(job)
            
# # # # #             return result
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error searching jobs: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_by_recruiter(recruiter_id):
# # # # #         """Get all jobs posted by a recruiter"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT j.*, 
# # # # #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as total_applications
# # # # #                 FROM jobs j
# # # # #                 WHERE j.recruiter_id = %s
# # # # #                 ORDER BY j.created_at DESC
# # # # #             """, (recruiter_id,))
            
# # # # #             jobs = cursor.fetchall()
# # # # #             return jobs
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting jobs by recruiter: {str(e)}")
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()


# # # # # class JobApplication:
# # # # #     @staticmethod
# # # # #     def create(job_id, freelancer_id, application_data):
# # # # #         """Create a new job application"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             # Check if already applied
# # # # #             cursor.execute("""
# # # # #                 SELECT id FROM job_applications 
# # # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # # #             """, (job_id, freelancer_id))
            
# # # # #             if cursor.fetchone():
# # # # #                 print(f"⚠️ Freelancer {freelancer_id} already applied to job {job_id}")
# # # # #                 return None
            
# # # # #             # Get freelancer profile ID
# # # # #             cursor.execute("""
# # # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # # #             """, (freelancer_id,))
# # # # #             profile = cursor.fetchone()
            
# # # # #             if not profile:
# # # # #                 print(f"❌ Freelancer profile not found for user {freelancer_id}")
# # # # #                 return None
            
# # # # #             # Create application
# # # # #             cursor.execute("""
# # # # #                 INSERT INTO job_applications (
# # # # #                     job_id, freelancer_id, freelancer_profile_id,
# # # # #                     cover_letter, proposed_rate, applied_at
# # # # #                 ) VALUES (%s, %s, %s, %s, %s, NOW())
# # # # #             """, (
# # # # #                 job_id, freelancer_id, profile['id'],
# # # # #                 application_data.get('cover_letter'),
# # # # #                 application_data.get('proposed_rate')
# # # # #             ))
            
# # # # #             application_id = cursor.lastrowid
            
# # # # #             # Update job applications count
# # # # #             cursor.execute("""
# # # # #                 UPDATE jobs SET applications_count = applications_count + 1
# # # # #                 WHERE id = %s
# # # # #             """, (job_id,))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ Application {application_id} created for job {job_id}")
# # # # #             return application_id
            
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error creating application: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def update_status(application_id, status, recruiter_notes=None):
# # # # #         """Update application status"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             # Get application details
# # # # #             cursor.execute("""
# # # # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # # # #                        u.email as freelancer_email,
# # # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # # # #                 FROM job_applications ja
# # # # #                 JOIN jobs j ON ja.job_id = j.id
# # # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # # #                 WHERE ja.id = %s
# # # # #             """, (application_id,))
            
# # # # #             application = cursor.fetchone()
            
# # # # #             if not application:
# # # # #                 print(f"❌ Application {application_id} not found")
# # # # #                 return None
            
# # # # #             # Update status
# # # # #             cursor.execute("""
# # # # #                 UPDATE job_applications 
# # # # #                 SET status = %s, recruiter_notes = %s, updated_at = NOW()
# # # # #                 WHERE id = %s
# # # # #             """, (status, recruiter_notes, application_id))
            
# # # # #             connection.commit()
# # # # #             print(f"✅ Application {application_id} status updated to {status}")
# # # # #             return application
            
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error updating application status: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_by_job(job_id):
# # # # #         """Get all applications for a job"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT ja.*, 
# # # # #                        fp.hourly_rate, fp.years_of_experience,
# # # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
# # # # #                        u.email as freelancer_email
# # # # #                 FROM job_applications ja
# # # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # # #                 JOIN freelancer_profiles fp ON ja.freelancer_profile_id = fp.id
# # # # #                 WHERE ja.job_id = %s
# # # # #                 ORDER BY ja.applied_at DESC
# # # # #             """, (job_id,))
            
# # # # #             applications = cursor.fetchall()
            
# # # # #             # Get skills for each applicant
# # # # #             for app in applications:
# # # # #                 cursor.execute("""
# # # # #                     SELECT s.name
# # # # #                     FROM freelancer_skills fs
# # # # #                     JOIN skills s ON fs.skill_id = s.id
# # # # #                     WHERE fs.freelancer_profile_id = %s
# # # # #                 """, (app['freelancer_profile_id'],))
# # # # #                 app['skills'] = [s['name'] for s in cursor.fetchall()]
            
# # # # #             return applications
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting applications by job: {str(e)}")
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_by_freelancer(freelancer_id):
# # # # #         """Get all applications by a freelancer"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
# # # # #                        rp.company_name
# # # # #                 FROM job_applications ja
# # # # #                 JOIN jobs j ON ja.job_id = j.id
# # # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # # #                 WHERE ja.freelancer_id = %s
# # # # #                 ORDER BY ja.applied_at DESC
# # # # #             """, (freelancer_id,))
            
# # # # #             applications = cursor.fetchall()
# # # # #             return applications
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting applications by freelancer: {str(e)}")
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()


# # # # # class Notification:
# # # # #     @staticmethod
# # # # #     def create(user_id, title, message, notification_type='application', 
# # # # #                related_application_id=None, related_job_id=None):
# # # # #         """Create a new notification"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             cursor.execute("""
# # # # #                 INSERT INTO notifications (
# # # # #                     user_id, title, message, notification_type,
# # # # #                     related_application_id, related_job_id, created_at
# # # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # # #             """, (user_id, title, message, notification_type, 
# # # # #                   related_application_id, related_job_id))
            
# # # # #             notification_id = cursor.lastrowid
# # # # #             connection.commit()
# # # # #             print(f"✅ Notification {notification_id} created for user {user_id}")
# # # # #             return notification_id
# # # # #         except Exception as e:
# # # # #             if connection:
# # # # #                 connection.rollback()
# # # # #             print(f"❌ Error creating notification: {str(e)}")
# # # # #             return None
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_by_user(user_id, unread_only=False, limit=50):
# # # # #         """Get notifications for a user"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             query = """
# # # # #                 SELECT * FROM notifications 
# # # # #                 WHERE user_id = %s
# # # # #             """
# # # # #             params = [user_id]
            
# # # # #             if unread_only:
# # # # #                 query += " AND is_read = FALSE"
            
# # # # #             query += " ORDER BY created_at DESC LIMIT %s"
# # # # #             params.append(limit)
            
# # # # #             cursor.execute(query, params)
# # # # #             notifications = cursor.fetchall()
# # # # #             return notifications
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting notifications: {str(e)}")
# # # # #             return []
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def mark_as_read(notification_id, user_id):
# # # # #         """Mark notification as read"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             cursor.execute("""
# # # # #                 UPDATE notifications 
# # # # #                 SET is_read = TRUE, read_at = NOW()
# # # # #                 WHERE id = %s AND user_id = %s
# # # # #             """, (notification_id, user_id))
            
# # # # #             affected = cursor.rowcount
# # # # #             connection.commit()
# # # # #             return affected > 0
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error marking notification as read: {str(e)}")
# # # # #             return False
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def mark_all_as_read(user_id):
# # # # #         """Mark all notifications as read for a user"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
            
# # # # #             cursor.execute("""
# # # # #                 UPDATE notifications 
# # # # #                 SET is_read = TRUE, read_at = NOW()
# # # # #                 WHERE user_id = %s AND is_read = FALSE
# # # # #             """, (user_id,))
            
# # # # #             affected = cursor.rowcount
# # # # #             connection.commit()
# # # # #             return affected
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error marking all notifications as read: {str(e)}")
# # # # #             return 0
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
    
# # # # #     @staticmethod
# # # # #     def get_unread_count(user_id):
# # # # #         """Get unread notifications count"""
# # # # #         connection = None
# # # # #         cursor = None
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor(dictionary=True)
            
# # # # #             cursor.execute("""
# # # # #                 SELECT COUNT(*) as count
# # # # #                 FROM notifications 
# # # # #                 WHERE user_id = %s AND is_read = FALSE
# # # # #             """, (user_id,))
            
# # # # #             result = cursor.fetchone()
# # # # #             return result['count'] if result else 0
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error getting unread count: {str(e)}")
# # # # #             return 0
# # # # #         finally:
# # # # #             if cursor:
# # # # #                 cursor.close()
# # # # #             if connection:
# # # # #                 connection.close()
# # # # # database/models.py

# # # # from database.db_config import get_db_connection
# # # # from utils.auth_utils import hash_password, check_password
# # # # from datetime import datetime
# # # # import traceback
# # # # import pymysql

# # # # class User:
# # # #     @staticmethod
# # # #     def create(username, email, password, first_name, last_name, user_type):
# # # #         """Create a new user"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             password_hash = hash_password(password)
            
# # # #             # Insert user with correct column names from your database
# # # #             cursor.execute("""
# # # #                 INSERT INTO users (
# # # #                     username, email, password_hash, first_name, last_name, 
# # # #                     user_type, is_verified, date_joined
# # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
# # # #             """, (
# # # #                 username, email, password_hash, first_name, last_name, 
# # # #                 user_type, False
# # # #             ))
            
# # # #             user_id = cursor.lastrowid
            
# # # #             # Create profile based on user type
# # # #             if user_type == 'freelancer':
# # # #                 cursor.execute("""
# # # #                     INSERT INTO freelancer_profiles (user_id, is_available)
# # # #                     VALUES (%s, %s)
# # # #                 """, (user_id, True))
# # # #             else:
# # # #                 cursor.execute("""
# # # #                     INSERT INTO recruiter_profiles (user_id, company_name)
# # # #                     VALUES (%s, %s)
# # # #                 """, (user_id, f"{first_name} {last_name}'s Company"))
            
# # # #             connection.commit()
# # # #             print(f"✅ User created successfully with ID: {user_id}")
# # # #             return user_id
            
# # # #         except pymysql.Error as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Database error creating user: {str(e)}")
# # # #             traceback.print_exc()
# # # #             raise e
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error creating user: {str(e)}")
# # # #             traceback.print_exc()
# # # #             raise e
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def find_by_email(email):
# # # #         """Find user by email"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT id, username, email, password_hash, first_name, last_name, 
# # # #                        user_type, is_verified, date_joined, profile_picture,
# # # #                        verification_token, email_verified_at
# # # #                 FROM users WHERE email = %s
# # # #             """, (email,))
            
# # # #             user = cursor.fetchone()
# # # #             return user
# # # #         except Exception as e:
# # # #             print(f"❌ Error finding user by email: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def find_by_id(user_id):
# # # #         """Find user by ID"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT id, username, email, first_name, last_name, 
# # # #                        user_type, is_verified, date_joined, profile_picture
# # # #                 FROM users WHERE id = %s
# # # #             """, (user_id,))
            
# # # #             user = cursor.fetchone()
# # # #             return user
# # # #         except Exception as e:
# # # #             print(f"❌ Error finding user by ID: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def find_by_verification_token(token):
# # # #         """Find user by verification token"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT id, username, email, first_name, last_name, 
# # # #                        user_type, is_verified
# # # #                 FROM users 
# # # #                 WHERE verification_token = %s 
# # # #                 AND date_joined > DATE_SUB(NOW(), INTERVAL 24 HOUR)
# # # #             """, (token,))
            
# # # #             user = cursor.fetchone()
# # # #             return user
# # # #         except Exception as e:
# # # #             print(f"❌ Error finding user by token: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def authenticate(email, password):
# # # #         """Authenticate user"""
# # # #         try:
# # # #             user = User.find_by_email(email)
# # # #             if user and check_password(password, user['password_hash']):
# # # #                 # Update last login
# # # #                 connection = get_db_connection()
# # # #                 cursor = connection.cursor()
# # # #                 cursor.execute("""
# # # #                     UPDATE users SET last_login = NOW() WHERE id = %s
# # # #                 """, (user['id'],))
# # # #                 connection.commit()
# # # #                 cursor.close()
# # # #                 connection.close()
                
# # # #                 # Remove password hash before returning
# # # #                 user.pop('password_hash', None)
# # # #                 return user
# # # #             return None
# # # #         except Exception as e:
# # # #             print(f"❌ Error authenticating user: {str(e)}")
# # # #             return None
    
# # # #     @staticmethod
# # # #     def set_verification_token(user_id, token):
# # # #         """Set email verification token"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 UPDATE users 
# # # #                 SET verification_token = %s
# # # #                 WHERE id = %s
# # # #             """, (token, user_id))
            
# # # #             connection.commit()
# # # #             print(f"✅ Verification token set for user {user_id}")
# # # #             return True
# # # #         except Exception as e:
# # # #             print(f"❌ Error setting verification token: {str(e)}")
# # # #             return False
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def verify_email(user_id):
# # # #         """Mark user email as verified"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 UPDATE users 
# # # #                 SET is_verified = TRUE, email_verified_at = NOW(), 
# # # #                     verification_token = NULL
# # # #                 WHERE id = %s
# # # #             """, (user_id,))
            
# # # #             connection.commit()
# # # #             print(f"✅ Email verified for user {user_id}")
# # # #             return True
# # # #         except Exception as e:
# # # #             print(f"❌ Error verifying email: {str(e)}")
# # # #             return False
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()


# # # # class FreelancerProfile:
# # # #     @staticmethod
# # # #     def get_by_user_id(user_id):
# # # #         """Get freelancer profile by user ID"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # #                        u.profile_picture, u.is_verified
# # # #                 FROM freelancer_profiles fp
# # # #                 JOIN users u ON fp.user_id = u.id
# # # #                 WHERE fp.user_id = %s
# # # #             """, (user_id,))
            
# # # #             profile = cursor.fetchone()
            
# # # #             if profile:
# # # #                 # Get skills
# # # #                 cursor.execute("""
# # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # #                     FROM freelancer_skills fs
# # # #                     JOIN skills s ON fs.skill_id = s.id
# # # #                     WHERE fs.freelancer_profile_id = %s
# # # #                 """, (profile['id'],))
# # # #                 profile['skills'] = cursor.fetchall()
                
# # # #                 # Get tech stacks
# # # #                 cursor.execute("""
# # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # #                     FROM freelancer_tech_stacks fts
# # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # #                     WHERE fts.freelancer_profile_id = %s
# # # #                 """, (profile['id'],))
# # # #                 profile['tech_stacks'] = cursor.fetchall()
            
# # # #             return profile
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting freelancer profile: {str(e)}")
# # # #             traceback.print_exc()
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def update_profile(user_id, profile_data):
# # # #         """Update freelancer profile"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             # Get profile ID
# # # #             cursor.execute("""
# # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # #             """, (user_id,))
# # # #             profile = cursor.fetchone()
            
# # # #             if not profile:
# # # #                 print(f"❌ Freelancer profile not found for user {user_id}")
# # # #                 return None
            
# # # #             profile_id = profile['id']
            
# # # #             # Update basic profile fields
# # # #             update_fields = []
# # # #             values = []
            
# # # #             allowed_fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # #                              'years_of_experience', 'github_url', 'linkedin_url', 
# # # #                              'portfolio_url', 'is_available']
            
# # # #             for field in allowed_fields:
# # # #                 if field in profile_data:
# # # #                     update_fields.append(f"{field} = %s")
# # # #                     values.append(profile_data[field])
            
# # # #             if update_fields:
# # # #                 values.append(profile_id)
# # # #                 query = f"""
# # # #                     UPDATE freelancer_profiles 
# # # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # # #                     WHERE id = %s
# # # #                 """
# # # #                 cursor.execute(query, values)
            
# # # #             # Update skills
# # # #             if 'skills' in profile_data:
# # # #                 # Delete existing skills
# # # #                 cursor.execute("""
# # # #                     DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s
# # # #                 """, (profile_id,))
                
# # # #                 # Add new skills
# # # #                 for skill in profile_data['skills']:
# # # #                     skill_name = skill.get('name') if isinstance(skill, dict) else skill
                    
# # # #                     # Get or create skill
# # # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # # #                     skill_record = cursor.fetchone()
# # # #                     if skill_record:
# # # #                         skill_id = skill_record['id']
# # # #                     else:
# # # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # # #                         skill_id = cursor.lastrowid
                    
# # # #                     proficiency = skill.get('proficiency_level', 'intermediate') if isinstance(skill, dict) else 'intermediate'
                    
# # # #                     cursor.execute("""
# # # #                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
# # # #                         VALUES (%s, %s, %s)
# # # #                     """, (profile_id, skill_id, proficiency))
            
# # # #             # Update tech stacks
# # # #             if 'tech_stacks' in profile_data:
# # # #                 # Delete existing tech stacks
# # # #                 cursor.execute("""
# # # #                     DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s
# # # #                 """, (profile_id,))
                
# # # #                 # Add new tech stacks
# # # #                 for tech in profile_data['tech_stacks']:
# # # #                     tech_name = tech.get('name') if isinstance(tech, dict) else tech
                    
# # # #                     # Get or create tech stack
# # # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # # #                     tech_record = cursor.fetchone()
# # # #                     if tech_record:
# # # #                         tech_id = tech_record['id']
# # # #                     else:
# # # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # # #                         tech_id = cursor.lastrowid
                    
# # # #                     experience = tech.get('experience_years', 0) if isinstance(tech, dict) else 0
                    
# # # #                     cursor.execute("""
# # # #                         INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
# # # #                         VALUES (%s, %s, %s)
# # # #                     """, (profile_id, tech_id, experience))
            
# # # #             connection.commit()
# # # #             print(f"✅ Freelancer profile updated for user {user_id}")
            
# # # #             return FreelancerProfile.get_by_user_id(user_id)
            
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error updating freelancer profile: {str(e)}")
# # # #             traceback.print_exc()
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def search_freelancers(filters):
# # # #         """Search freelancers based on skills, rate, experience"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             query = """
# # # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # # #                        u.date_joined
# # # #                 FROM freelancer_profiles fp
# # # #                 JOIN users u ON fp.user_id = u.id
# # # #                 WHERE u.is_active = TRUE AND fp.is_available = TRUE
# # # #             """
# # # #             params = []
            
# # # #             if filters.get('min_hourly_rate'):
# # # #                 query += " AND fp.hourly_rate >= %s"
# # # #                 params.append(filters['min_hourly_rate'])
            
# # # #             if filters.get('max_hourly_rate'):
# # # #                 query += " AND fp.hourly_rate <= %s"
# # # #                 params.append(filters['max_hourly_rate'])
            
# # # #             if filters.get('years_experience_min'):
# # # #                 query += " AND fp.years_of_experience >= %s"
# # # #                 params.append(filters['years_experience_min'])
            
# # # #             if filters.get('skill'):
# # # #                 query += """ AND fp.id IN (
# # # #                     SELECT fs.freelancer_profile_id 
# # # #                     FROM freelancer_skills fs
# # # #                     JOIN skills s ON fs.skill_id = s.id
# # # #                     WHERE s.name LIKE %s
# # # #                 )"""
# # # #                 params.append(f'%{filters["skill"]}%')
            
# # # #             query += " ORDER BY fp.created_at DESC LIMIT 50"
            
# # # #             cursor.execute(query, params)
# # # #             freelancers = cursor.fetchall()
            
# # # #             # Get skills and tech stacks for each freelancer
# # # #             result = []
# # # #             for freelancer in freelancers:
# # # #                 # Get skills
# # # #                 cursor.execute("""
# # # #                     SELECT s.id, s.name, fs.proficiency_level
# # # #                     FROM freelancer_skills fs
# # # #                     JOIN skills s ON fs.skill_id = s.id
# # # #                     WHERE fs.freelancer_profile_id = %s
# # # #                 """, (freelancer['id'],))
# # # #                 freelancer['skills'] = cursor.fetchall()
                
# # # #                 # Get tech stacks
# # # #                 cursor.execute("""
# # # #                     SELECT ts.id, ts.name, fts.experience_years
# # # #                     FROM freelancer_tech_stacks fts
# # # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # # #                     WHERE fts.freelancer_profile_id = %s
# # # #                 """, (freelancer['id'],))
# # # #                 freelancer['tech_stacks'] = cursor.fetchall()
                
# # # #                 result.append(freelancer)
            
# # # #             return result
# # # #         except Exception as e:
# # # #             print(f"❌ Error searching freelancers: {str(e)}")
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()


# # # # class RecruiterProfile:
# # # #     @staticmethod
# # # #     def get_by_user_id(user_id):
# # # #         """Get recruiter profile by user ID"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT rp.*, u.username, u.email, u.first_name, u.last_name
# # # #                 FROM recruiter_profiles rp
# # # #                 JOIN users u ON rp.user_id = u.id
# # # #                 WHERE rp.user_id = %s
# # # #             """, (user_id,))
            
# # # #             profile = cursor.fetchone()
# # # #             return profile
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting recruiter profile: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def update_profile(user_id, profile_data):
# # # #         """Update recruiter profile"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             update_fields = []
# # # #             values = []
            
# # # #             allowed_fields = ['company_name', 'company_website', 'company_size', 
# # # #                              'industry', 'company_description', 'location', 'phone']
            
# # # #             for field in allowed_fields:
# # # #                 if field in profile_data:
# # # #                     update_fields.append(f"{field} = %s")
# # # #                     values.append(profile_data[field])
            
# # # #             if update_fields:
# # # #                 values.append(user_id)
# # # #                 query = f"""
# # # #                     UPDATE recruiter_profiles 
# # # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # # #                     WHERE user_id = %s
# # # #                 """
# # # #                 cursor.execute(query, values)
# # # #                 connection.commit()
# # # #                 print(f"✅ Recruiter profile updated for user {user_id}")
            
# # # #             return RecruiterProfile.get_by_user_id(user_id)
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error updating recruiter profile: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()


# # # # class Job:
# # # #     @staticmethod
# # # #     def create(recruiter_id, job_data):
# # # #         """Create a new job posting"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             # Get recruiter profile ID
# # # #             cursor.execute("""
# # # #                 SELECT id FROM recruiter_profiles WHERE user_id = %s
# # # #             """, (recruiter_id,))
# # # #             profile = cursor.fetchone()
            
# # # #             if not profile:
# # # #                 print(f"❌ Recruiter profile not found for user {recruiter_id}")
# # # #                 return None
            
# # # #             profile_id = profile['id']
            
# # # #             # Insert job
# # # #             cursor.execute("""
# # # #                 INSERT INTO jobs (
# # # #                     recruiter_id, recruiter_profile_id, title, description,
# # # #                     pay_per_hour, experience_level, job_type, location,
# # # #                     is_remote, requirements, responsibilities, benefits,
# # # #                     application_deadline, created_at
# # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
# # # #             """, (
# # # #                 recruiter_id, profile_id, job_data['title'],
# # # #                 job_data['description'], job_data['pay_per_hour'],
# # # #                 job_data['experience_level'], job_data.get('job_type', 'freelance'),
# # # #                 job_data.get('location'), job_data.get('is_remote', True),
# # # #                 job_data.get('requirements'), job_data.get('responsibilities'),
# # # #                 job_data.get('benefits'), job_data.get('application_deadline')
# # # #             ))
            
# # # #             job_id = cursor.lastrowid
# # # #             print(f"✅ Job created with ID: {job_id}")
            
# # # #             # Add required skills
# # # #             if 'required_skills' in job_data and job_data['required_skills']:
# # # #                 for skill_name in job_data['required_skills']:
# # # #                     # Get or create skill
# # # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # # #                     skill = cursor.fetchone()
# # # #                     if skill:
# # # #                         skill_id = skill['id']
# # # #                     else:
# # # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # # #                         skill_id = cursor.lastrowid
                    
# # # #                     cursor.execute("""
# # # #                         INSERT INTO job_skills (job_id, skill_id, is_required)
# # # #                         VALUES (%s, %s, TRUE)
# # # #                     """, (job_id, skill_id))
            
# # # #             # Add tech stack
# # # #             if 'tech_stack' in job_data and job_data['tech_stack']:
# # # #                 for tech_name in job_data['tech_stack']:
# # # #                     # Get or create tech stack
# # # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # # #                     tech = cursor.fetchone()
# # # #                     if tech:
# # # #                         tech_id = tech['id']
# # # #                     else:
# # # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # # #                         tech_id = cursor.lastrowid
                    
# # # #                     cursor.execute("""
# # # #                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
# # # #                         VALUES (%s, %s, TRUE)
# # # #                     """, (job_id, tech_id))
            
# # # #             connection.commit()
# # # #             return job_id
            
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error creating job: {str(e)}")
# # # #             traceback.print_exc()
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_by_id(job_id):
# # # #         """Get job by ID"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT j.*, rp.company_name, u.email as recruiter_email,
# # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # #                 FROM jobs j
# # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # #                 JOIN users u ON j.recruiter_id = u.id
# # # #                 WHERE j.id = %s
# # # #             """, (job_id,))
            
# # # #             job = cursor.fetchone()
            
# # # #             if job:
# # # #                 # Get required skills
# # # #                 cursor.execute("""
# # # #                     SELECT s.id, s.name
# # # #                     FROM job_skills js
# # # #                     JOIN skills s ON js.skill_id = s.id
# # # #                     WHERE js.job_id = %s AND js.is_required = TRUE
# # # #                 """, (job_id,))
# # # #                 job['required_skills'] = [skill['name'] for skill in cursor.fetchall()]
                
# # # #                 # Get tech stack
# # # #                 cursor.execute("""
# # # #                     SELECT ts.id, ts.name
# # # #                     FROM job_tech_stacks jts
# # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # #                     WHERE jts.job_id = %s AND jts.is_required = TRUE
# # # #                 """, (job_id,))
# # # #                 job['tech_stack'] = [tech['name'] for tech in cursor.fetchall()]
                
# # # #                 # Increment view count
# # # #                 cursor.execute("""
# # # #                     UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
# # # #                 """, (job_id,))
# # # #                 connection.commit()
            
# # # #             return job
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting job by ID: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def search_jobs(filters):
# # # #         """Search jobs with filters"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             query = """
# # # #                 SELECT j.*, rp.company_name,
# # # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # # #                 FROM jobs j
# # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # #                 JOIN users u ON j.recruiter_id = u.id
# # # #                 WHERE j.is_active = TRUE
# # # #             """
# # # #             params = []
            
# # # #             if filters.get('search'):
# # # #                 search_term = f'%{filters["search"]}%'
# # # #                 query += """ AND (
# # # #                     LOWER(j.title) LIKE LOWER(%s) OR 
# # # #                     LOWER(j.description) LIKE LOWER(%s) OR 
# # # #                     LOWER(j.requirements) LIKE LOWER(%s)
# # # #                 )"""
# # # #                 params.extend([search_term, search_term, search_term])
            
# # # #             if filters.get('experience_level'):
# # # #                 query += " AND j.experience_level = %s"
# # # #                 params.append(filters['experience_level'])
            
# # # #             if filters.get('min_pay'):
# # # #                 try:
# # # #                     min_pay = float(filters['min_pay'])
# # # #                     query += " AND j.pay_per_hour >= %s"
# # # #                     params.append(min_pay)
# # # #                 except (ValueError, TypeError):
# # # #                     pass
            
# # # #             if filters.get('max_pay'):
# # # #                 try:
# # # #                     max_pay = float(filters['max_pay'])
# # # #                     query += " AND j.pay_per_hour <= %s"
# # # #                     params.append(max_pay)
# # # #                 except (ValueError, TypeError):
# # # #                     pass
            
# # # #             if filters.get('job_type'):
# # # #                 query += " AND j.job_type = %s"
# # # #                 params.append(filters['job_type'])
            
# # # #             if filters.get('is_remote'):
# # # #                 query += " AND j.is_remote = TRUE"
            
# # # #             query += " ORDER BY j.created_at DESC"
            
# # # #             cursor.execute(query, params)
# # # #             jobs = cursor.fetchall()
            
# # # #             # Get skills and tech stack for each job
# # # #             result = []
# # # #             for job in jobs:
# # # #                 cursor.execute("""
# # # #                     SELECT s.name
# # # #                     FROM job_skills js
# # # #                     JOIN skills s ON js.skill_id = s.id
# # # #                     WHERE js.job_id = %s
# # # #                 """, (job['id'],))
# # # #                 job['required_skills'] = [skill['name'] for skill in cursor.fetchall()]
                
# # # #                 cursor.execute("""
# # # #                     SELECT ts.name
# # # #                     FROM job_tech_stacks jts
# # # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # # #                     WHERE jts.job_id = %s
# # # #                 """, (job['id'],))
# # # #                 job['tech_stack'] = [tech['name'] for tech in cursor.fetchall()]
                
# # # #                 result.append(job)
            
# # # #             return result
# # # #         except Exception as e:
# # # #             print(f"❌ Error searching jobs: {str(e)}")
# # # #             traceback.print_exc()
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_by_recruiter(recruiter_id):
# # # #         """Get all jobs posted by a recruiter"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT j.*, 
# # # #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as total_applications
# # # #                 FROM jobs j
# # # #                 WHERE j.recruiter_id = %s
# # # #                 ORDER BY j.created_at DESC
# # # #             """, (recruiter_id,))
            
# # # #             jobs = cursor.fetchall()
# # # #             return jobs
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting jobs by recruiter: {str(e)}")
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()


# # # # class JobApplication:
# # # #     @staticmethod
# # # #     def create(job_id, freelancer_id, application_data):
# # # #         """Create a new job application"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             # Check if already applied
# # # #             cursor.execute("""
# # # #                 SELECT id FROM job_applications 
# # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # #             """, (job_id, freelancer_id))
            
# # # #             if cursor.fetchone():
# # # #                 print(f"⚠️ Freelancer {freelancer_id} already applied to job {job_id}")
# # # #                 return None
            
# # # #             # Get freelancer profile ID
# # # #             cursor.execute("""
# # # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # # #             """, (freelancer_id,))
# # # #             profile = cursor.fetchone()
            
# # # #             if not profile:
# # # #                 print(f"❌ Freelancer profile not found for user {freelancer_id}")
# # # #                 return None
            
# # # #             profile_id = profile['id']
            
# # # #             # Create application
# # # #             cursor.execute("""
# # # #                 INSERT INTO job_applications (
# # # #                     job_id, freelancer_id, freelancer_profile_id,
# # # #                     cover_letter, proposed_rate, applied_at
# # # #                 ) VALUES (%s, %s, %s, %s, %s, NOW())
# # # #             """, (
# # # #                 job_id, freelancer_id, profile_id,
# # # #                 application_data.get('cover_letter'),
# # # #                 application_data.get('proposed_rate')
# # # #             ))
            
# # # #             application_id = cursor.lastrowid
            
# # # #             # Update job applications count
# # # #             cursor.execute("""
# # # #                 UPDATE jobs SET applications_count = applications_count + 1
# # # #                 WHERE id = %s
# # # #             """, (job_id,))
            
# # # #             connection.commit()
# # # #             print(f"✅ Application {application_id} created for job {job_id}")
# # # #             return application_id
            
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error creating application: {str(e)}")
# # # #             traceback.print_exc()
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def update_status(application_id, status, recruiter_notes=None):
# # # #         """Update application status"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             # Get application details
# # # #             cursor.execute("""
# # # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # # #                        u.email as freelancer_email,
# # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # # #                 FROM job_applications ja
# # # #                 JOIN jobs j ON ja.job_id = j.id
# # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # #                 WHERE ja.id = %s
# # # #             """, (application_id,))
            
# # # #             application = cursor.fetchone()
            
# # # #             if not application:
# # # #                 print(f"❌ Application {application_id} not found")
# # # #                 return None
            
# # # #             # Update status
# # # #             cursor.execute("""
# # # #                 UPDATE job_applications 
# # # #                 SET status = %s, recruiter_notes = %s, updated_at = NOW()
# # # #                 WHERE id = %s
# # # #             """, (status, recruiter_notes, application_id))
            
# # # #             connection.commit()
# # # #             print(f"✅ Application {application_id} status updated to {status}")
            
# # # #             # Fetch updated application
# # # #             cursor.execute("""
# # # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # # #                        u.email as freelancer_email,
# # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # # #                 FROM job_applications ja
# # # #                 JOIN jobs j ON ja.job_id = j.id
# # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # #                 WHERE ja.id = %s
# # # #             """, (application_id,))
# # # #             return cursor.fetchone()
            
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error updating application status: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_by_job(job_id):
# # # #         """Get all applications for a job"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT ja.*, 
# # # #                        fp.hourly_rate, fp.years_of_experience,
# # # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
# # # #                        u.email as freelancer_email
# # # #                 FROM job_applications ja
# # # #                 JOIN users u ON ja.freelancer_id = u.id
# # # #                 JOIN freelancer_profiles fp ON ja.freelancer_profile_id = fp.id
# # # #                 WHERE ja.job_id = %s
# # # #                 ORDER BY ja.applied_at DESC
# # # #             """, (job_id,))
            
# # # #             applications = cursor.fetchall()
            
# # # #             # Get skills for each applicant
# # # #             for app in applications:
# # # #                 cursor.execute("""
# # # #                     SELECT s.name
# # # #                     FROM freelancer_skills fs
# # # #                     JOIN skills s ON fs.skill_id = s.id
# # # #                     WHERE fs.freelancer_profile_id = %s
# # # #                 """, (app['freelancer_profile_id'],))
# # # #                 app['skills'] = [skill['name'] for skill in cursor.fetchall()]
            
# # # #             return applications
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting applications by job: {str(e)}")
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_by_freelancer(freelancer_id):
# # # #         """Get all applications by a freelancer"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
# # # #                        rp.company_name
# # # #                 FROM job_applications ja
# # # #                 JOIN jobs j ON ja.job_id = j.id
# # # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # # #                 WHERE ja.freelancer_id = %s
# # # #                 ORDER BY ja.applied_at DESC
# # # #             """, (freelancer_id,))
            
# # # #             applications = cursor.fetchall()
# # # #             return applications
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting applications by freelancer: {str(e)}")
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()


# # # # class Notification:
# # # #     @staticmethod
# # # #     def create(user_id, title, message, notification_type='application', 
# # # #                related_application_id=None, related_job_id=None):
# # # #         """Create a new notification"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 INSERT INTO notifications (
# # # #                     user_id, title, message, notification_type,
# # # #                     related_application_id, related_job_id, created_at
# # # #                 ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # #             """, (user_id, title, message, notification_type, 
# # # #                   related_application_id, related_job_id))
            
# # # #             notification_id = cursor.lastrowid
# # # #             connection.commit()
# # # #             print(f"✅ Notification {notification_id} created for user {user_id}")
# # # #             return notification_id
# # # #         except Exception as e:
# # # #             if connection:
# # # #                 connection.rollback()
# # # #             print(f"❌ Error creating notification: {str(e)}")
# # # #             return None
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_by_user(user_id, unread_only=False, limit=50):
# # # #         """Get notifications for a user"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             query = """
# # # #                 SELECT * FROM notifications 
# # # #                 WHERE user_id = %s
# # # #             """
# # # #             params = [user_id]
            
# # # #             if unread_only:
# # # #                 query += " AND is_read = FALSE"
            
# # # #             query += " ORDER BY created_at DESC LIMIT %s"
# # # #             params.append(limit)
            
# # # #             cursor.execute(query, params)
# # # #             notifications = cursor.fetchall()
# # # #             return notifications
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting notifications: {str(e)}")
# # # #             return []
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def mark_as_read(notification_id, user_id):
# # # #         """Mark notification as read"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 UPDATE notifications 
# # # #                 SET is_read = TRUE, read_at = NOW()
# # # #                 WHERE id = %s AND user_id = %s
# # # #             """, (notification_id, user_id))
            
# # # #             affected = cursor.rowcount
# # # #             connection.commit()
# # # #             return affected > 0
# # # #         except Exception as e:
# # # #             print(f"❌ Error marking notification as read: {str(e)}")
# # # #             return False
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def mark_all_as_read(user_id):
# # # #         """Mark all notifications as read for a user"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 UPDATE notifications 
# # # #                 SET is_read = TRUE, read_at = NOW()
# # # #                 WHERE user_id = %s AND is_read = FALSE
# # # #             """, (user_id,))
            
# # # #             affected = cursor.rowcount
# # # #             connection.commit()
# # # #             return affected
# # # #         except Exception as e:
# # # #             print(f"❌ Error marking all notifications as read: {str(e)}")
# # # #             return 0
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()
    
# # # #     @staticmethod
# # # #     def get_unread_count(user_id):
# # # #         """Get unread notifications count"""
# # # #         connection = None
# # # #         cursor = None
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
            
# # # #             cursor.execute("""
# # # #                 SELECT COUNT(*) as count
# # # #                 FROM notifications 
# # # #                 WHERE user_id = %s AND is_read = FALSE
# # # #             """, (user_id,))
            
# # # #             result = cursor.fetchone()
# # # #             return result['count'] if result else 0
# # # #         except Exception as e:
# # # #             print(f"❌ Error getting unread count: {str(e)}")
# # # #             return 0
# # # #         finally:
# # # #             if cursor:
# # # #                 cursor.close()
# # # #             if connection:
# # # #                 connection.close()



# # # # database/models.py

# # # from database.db_config import get_db_connection
# # # from utils.auth_utils import hash_password, check_password
# # # from datetime import datetime
# # # import traceback
# # # import pymysql

# # # class User:
# # #     @staticmethod
# # #     def create(username, email, password, first_name, last_name, user_type):
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             password_hash = hash_password(password)

# # #             cursor.execute("""
# # #                 INSERT INTO users (
# # #                     username, email, password_hash, first_name, last_name,
# # #                     user_type, is_verified, date_joined
# # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
# # #             """, (username, email, password_hash, first_name, last_name, user_type, False))

# # #             user_id = cursor.lastrowid

# # #             if user_type == 'freelancer':
# # #                 cursor.execute("INSERT INTO freelancer_profiles (user_id, is_available) VALUES (%s, %s)", (user_id, True))
# # #             else:
# # #                 cursor.execute("INSERT INTO recruiter_profiles (user_id, company_name) VALUES (%s, %s)",
# # #                                (user_id, f"{first_name} {last_name}'s Company"))

# # #             connection.commit()
# # #             return user_id
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             traceback.print_exc()
# # #             raise e
# # #         finally:
# # #             if cursor: cursor.close()
# # #             if connection: connection.close()

# # #     @staticmethod
# # #     def find_by_email(email):
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("""
# # #                 SELECT id, username, email, password_hash, first_name, last_name,
# # #                        user_type, is_verified, date_joined, profile_picture,
# # #                        verification_token, email_verified_at
# # #                 FROM users WHERE email = %s
# # #             """, (email,))
# # #             return cursor.fetchone()
# # #         except Exception as e:
# # #             print(f"❌ Error finding user by email: {e}")
# # #             return None
# # #         finally:
# # #             if cursor: cursor.close()
# # #             if connection: connection.close()

# # #     @staticmethod
# # #     def find_by_id(user_id):
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("""
# # #                 SELECT id, username, email, first_name, last_name,
# # #                        user_type, is_verified, date_joined, profile_picture
# # #                 FROM users WHERE id = %s
# # #             """, (user_id,))
# # #             return cursor.fetchone()
# # #         except Exception as e:
# # #             print(f"❌ Error finding user by ID: {e}")
# # #             return None
# # #         finally:
# # #             if cursor: cursor.close()
# # #             if connection: connection.close()

# # #     @staticmethod
# # #     def authenticate(email, password):
# # #         try:
# # #             user = User.find_by_email(email)
# # #             if user and check_password(password, user['password_hash']):
# # #                 conn = get_db_connection()
# # #                 cur = conn.cursor()
# # #                 cur.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
# # #                 conn.commit()
# # #                 cur.close()
# # #                 conn.close()
# # #                 user.pop('password_hash', None)
# # #                 return user
# # #             return None
# # #         except Exception as e:
# # #             print(f"❌ Error authenticating user: {e}")
# # #             return None

# # #     @staticmethod
# # #     def set_verification_token(user_id, token):
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("UPDATE users SET verification_token = %s WHERE id = %s", (token, user_id))
# # #             connection.commit()
# # #             return True
# # #         except Exception as e:
# # #             print(f"❌ Error setting token: {e}")
# # #             return False
# # #         finally:
# # #             if cursor: cursor.close()
# # #             if connection: connection.close()

# # #     @staticmethod
# # #     def verify_email(user_id):
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("""
# # #                 UPDATE users SET is_verified = TRUE, email_verified_at = NOW(),
# # #                     verification_token = NULL WHERE id = %s
# # #             """, (user_id,))
# # #             connection.commit()
# # #             return True
# # #         except Exception as e:
# # #             print(f"❌ Error verifying email: {e}")
# # #             return False
# # #         finally:
# # #             if cursor: cursor.close()
# # #             if connection: connection.close()


# # # class FreelancerProfile:
# # #     @staticmethod
# # #     def get_by_user_id(user_id):
# # #         """Get freelancer profile by user ID"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # #                        u.profile_picture, u.is_verified
# # #                 FROM freelancer_profiles fp
# # #                 JOIN users u ON fp.user_id = u.id
# # #                 WHERE fp.user_id = %s
# # #             """, (user_id,))
            
# # #             profile = cursor.fetchone()
            
# # #             if profile:
# # #                 # Get skills
# # #                 cursor.execute("""
# # #                     SELECT s.id, s.name, fs.proficiency_level
# # #                     FROM freelancer_skills fs
# # #                     JOIN skills s ON fs.skill_id = s.id
# # #                     WHERE fs.freelancer_profile_id = %s
# # #                 """, (profile['id'],))
# # #                 profile['skills'] = cursor.fetchall()
                
# # #                 # Get tech stacks
# # #                 cursor.execute("""
# # #                     SELECT ts.id, ts.name, fts.experience_years
# # #                     FROM freelancer_tech_stacks fts
# # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # #                     WHERE fts.freelancer_profile_id = %s
# # #                 """, (profile['id'],))
# # #                 profile['tech_stacks'] = cursor.fetchall()
            
# # #             return profile
# # #         except Exception as e:
# # #             print(f"❌ Error getting freelancer profile: {str(e)}")
# # #             traceback.print_exc()
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def update_profile(user_id, profile_data):
# # #         """Update freelancer profile"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             # Get profile ID
# # #             cursor.execute("""
# # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # #             """, (user_id,))
# # #             profile = cursor.fetchone()
            
# # #             if not profile:
# # #                 print(f"❌ Freelancer profile not found for user {user_id}")
# # #                 return None
            
# # #             profile_id = profile['id']
            
# # #             # Update basic profile fields
# # #             update_fields = []
# # #             values = []
            
# # #             allowed_fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # #                              'years_of_experience', 'github_url', 'linkedin_url', 
# # #                              'portfolio_url', 'is_available']
            
# # #             for field in allowed_fields:
# # #                 if field in profile_data:
# # #                     update_fields.append(f"{field} = %s")
# # #                     values.append(profile_data[field])
            
# # #             if update_fields:
# # #                 values.append(profile_id)
# # #                 query = f"""
# # #                     UPDATE freelancer_profiles 
# # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # #                     WHERE id = %s
# # #                 """
# # #                 cursor.execute(query, values)
            
# # #             # Update skills
# # #             if 'skills' in profile_data:
# # #                 # Delete existing skills
# # #                 cursor.execute("""
# # #                     DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s
# # #                 """, (profile_id,))
                
# # #                 # Add new skills
# # #                 for skill in profile_data['skills']:
# # #                     skill_name = skill.get('name') if isinstance(skill, dict) else skill
                    
# # #                     # Get or create skill
# # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # #                     skill_record = cursor.fetchone()
# # #                     if skill_record:
# # #                         skill_id = skill_record['id']
# # #                     else:
# # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # #                         skill_id = cursor.lastrowid
                    
# # #                     proficiency = skill.get('proficiency_level', 'intermediate') if isinstance(skill, dict) else 'intermediate'
                    
# # #                     cursor.execute("""
# # #                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
# # #                         VALUES (%s, %s, %s)
# # #                     """, (profile_id, skill_id, proficiency))
            
# # #             # Update tech stacks
# # #             if 'tech_stacks' in profile_data:
# # #                 # Delete existing tech stacks
# # #                 cursor.execute("""
# # #                     DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s
# # #                 """, (profile_id,))
                
# # #                 # Add new tech stacks
# # #                 for tech in profile_data['tech_stacks']:
# # #                     tech_name = tech.get('name') if isinstance(tech, dict) else tech
                    
# # #                     # Get or create tech stack
# # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # #                     tech_record = cursor.fetchone()
# # #                     if tech_record:
# # #                         tech_id = tech_record['id']
# # #                     else:
# # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # #                         tech_id = cursor.lastrowid
                    
# # #                     experience = tech.get('experience_years', 0) if isinstance(tech, dict) else 0
                    
# # #                     cursor.execute("""
# # #                         INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
# # #                         VALUES (%s, %s, %s)
# # #                     """, (profile_id, tech_id, experience))
            
# # #             connection.commit()
# # #             print(f"✅ Freelancer profile updated for user {user_id}")
            
# # #             return FreelancerProfile.get_by_user_id(user_id)
            
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ Error updating freelancer profile: {str(e)}")
# # #             traceback.print_exc()
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def search_freelancers(filters):
# # #         """Search freelancers based on skills, rate, experience"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             query = """
# # #                 SELECT fp.*, u.username, u.email, u.first_name, u.last_name,
# # #                        u.date_joined
# # #                 FROM freelancer_profiles fp
# # #                 JOIN users u ON fp.user_id = u.id
# # #                 WHERE u.is_active = TRUE AND fp.is_available = TRUE
# # #             """
# # #             params = []
            
# # #             if filters.get('min_hourly_rate'):
# # #                 query += " AND fp.hourly_rate >= %s"
# # #                 params.append(filters['min_hourly_rate'])
            
# # #             if filters.get('max_hourly_rate'):
# # #                 query += " AND fp.hourly_rate <= %s"
# # #                 params.append(filters['max_hourly_rate'])
            
# # #             if filters.get('years_experience_min'):
# # #                 query += " AND fp.years_of_experience >= %s"
# # #                 params.append(filters['years_experience_min'])
            
# # #             if filters.get('skill'):
# # #                 query += """ AND fp.id IN (
# # #                     SELECT fs.freelancer_profile_id 
# # #                     FROM freelancer_skills fs
# # #                     JOIN skills s ON fs.skill_id = s.id
# # #                     WHERE s.name LIKE %s
# # #                 )"""
# # #                 params.append(f'%{filters["skill"]}%')
            
# # #             query += " ORDER BY fp.created_at DESC LIMIT 50"
            
# # #             cursor.execute(query, params)
# # #             freelancers = cursor.fetchall()
            
# # #             # Get skills and tech stacks for each freelancer
# # #             result = []
# # #             for freelancer in freelancers:
# # #                 # Get skills
# # #                 cursor.execute("""
# # #                     SELECT s.id, s.name, fs.proficiency_level
# # #                     FROM freelancer_skills fs
# # #                     JOIN skills s ON fs.skill_id = s.id
# # #                     WHERE fs.freelancer_profile_id = %s
# # #                 """, (freelancer['id'],))
# # #                 freelancer['skills'] = cursor.fetchall()
                
# # #                 # Get tech stacks
# # #                 cursor.execute("""
# # #                     SELECT ts.id, ts.name, fts.experience_years
# # #                     FROM freelancer_tech_stacks fts
# # #                     JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# # #                     WHERE fts.freelancer_profile_id = %s
# # #                 """, (freelancer['id'],))
# # #                 freelancer['tech_stacks'] = cursor.fetchall()
                
# # #                 result.append(freelancer)
            
# # #             return result
# # #         except Exception as e:
# # #             print(f"❌ Error searching freelancers: {str(e)}")
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()


# # # class RecruiterProfile:
# # #     @staticmethod
# # #     def get_by_user_id(user_id):
# # #         """Get recruiter profile by user ID"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT rp.*, u.username, u.email, u.first_name, u.last_name
# # #                 FROM recruiter_profiles rp
# # #                 JOIN users u ON rp.user_id = u.id
# # #                 WHERE rp.user_id = %s
# # #             """, (user_id,))
            
# # #             profile = cursor.fetchone()
# # #             return profile
# # #         except Exception as e:
# # #             print(f"❌ Error getting recruiter profile: {str(e)}")
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def update_profile(user_id, profile_data):
# # #         """Update recruiter profile"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             update_fields = []
# # #             values = []
            
# # #             allowed_fields = ['company_name', 'company_website', 'company_size', 
# # #                              'industry', 'company_description', 'location', 'phone']
            
# # #             for field in allowed_fields:
# # #                 if field in profile_data:
# # #                     update_fields.append(f"{field} = %s")
# # #                     values.append(profile_data[field])
            
# # #             if update_fields:
# # #                 values.append(user_id)
# # #                 query = f"""
# # #                     UPDATE recruiter_profiles 
# # #                     SET {', '.join(update_fields)}, updated_at = NOW()
# # #                     WHERE user_id = %s
# # #                 """
# # #                 cursor.execute(query, values)
# # #                 connection.commit()
# # #                 print(f"✅ Recruiter profile updated for user {user_id}")
            
# # #             return RecruiterProfile.get_by_user_id(user_id)
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ Error updating recruiter profile: {str(e)}")
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()


# # # class Job:
# # #     @staticmethod
# # #     def create(recruiter_id, job_data):
# # #         """Create a new job posting"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             # Get recruiter profile ID
# # #             cursor.execute("""
# # #                 SELECT id FROM recruiter_profiles WHERE user_id = %s
# # #             """, (recruiter_id,))
# # #             profile = cursor.fetchone()
            
# # #             if not profile:
# # #                 print(f"❌ Recruiter profile not found for user {recruiter_id}")
# # #                 return None
            
# # #             profile_id = profile['id']
            
# # #             # Insert job
# # #             cursor.execute("""
# # #                 INSERT INTO jobs (
# # #                     recruiter_id, recruiter_profile_id, title, description,
# # #                     pay_per_hour, experience_level, job_type, location,
# # #                     is_remote, requirements, responsibilities, benefits,
# # #                     application_deadline, created_at
# # #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
# # #             """, (
# # #                 recruiter_id, profile_id, job_data['title'],
# # #                 job_data['description'], job_data['pay_per_hour'],
# # #                 job_data['experience_level'], job_data.get('job_type', 'freelance'),
# # #                 job_data.get('location'), job_data.get('is_remote', True),
# # #                 job_data.get('requirements'), job_data.get('responsibilities'),
# # #                 job_data.get('benefits'), job_data.get('application_deadline')
# # #             ))
            
# # #             job_id = cursor.lastrowid
# # #             print(f"✅ Job created with ID: {job_id}")
            
# # #             # Add required skills
# # #             if 'required_skills' in job_data and job_data['required_skills']:
# # #                 for skill_name in job_data['required_skills']:
# # #                     # Get or create skill
# # #                     cursor.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# # #                     skill = cursor.fetchone()
# # #                     if skill:
# # #                         skill_id = skill['id']
# # #                     else:
# # #                         cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# # #                         skill_id = cursor.lastrowid
                    
# # #                     cursor.execute("""
# # #                         INSERT INTO job_skills (job_id, skill_id, is_required)
# # #                         VALUES (%s, %s, TRUE)
# # #                     """, (job_id, skill_id))
            
# # #             # Add tech stack
# # #             if 'tech_stack' in job_data and job_data['tech_stack']:
# # #                 for tech_name in job_data['tech_stack']:
# # #                     # Get or create tech stack
# # #                     cursor.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# # #                     tech = cursor.fetchone()
# # #                     if tech:
# # #                         tech_id = tech['id']
# # #                     else:
# # #                         cursor.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# # #                         tech_id = cursor.lastrowid
                    
# # #                     cursor.execute("""
# # #                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
# # #                         VALUES (%s, %s, TRUE)
# # #                     """, (job_id, tech_id))
            
# # #             connection.commit()
# # #             return job_id
            
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ Error creating job: {str(e)}")
# # #             traceback.print_exc()
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_by_id(job_id):
# # #         """Get job by ID"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT j.*, rp.company_name, u.email as recruiter_email,
# # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # #                 FROM jobs j
# # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # #                 JOIN users u ON j.recruiter_id = u.id
# # #                 WHERE j.id = %s
# # #             """, (job_id,))
            
# # #             job = cursor.fetchone()
            
# # #             if job:
# # #                 # Get required skills
# # #                 cursor.execute("""
# # #                     SELECT s.id, s.name
# # #                     FROM job_skills js
# # #                     JOIN skills s ON js.skill_id = s.id
# # #                     WHERE js.job_id = %s AND js.is_required = TRUE
# # #                 """, (job_id,))
# # #                 job['required_skills'] = [skill['name'] for skill in cursor.fetchall()]
                
# # #                 # Get tech stack
# # #                 cursor.execute("""
# # #                     SELECT ts.id, ts.name
# # #                     FROM job_tech_stacks jts
# # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # #                     WHERE jts.job_id = %s AND jts.is_required = TRUE
# # #                 """, (job_id,))
# # #                 job['tech_stack'] = [tech['name'] for tech in cursor.fetchall()]
                
# # #                 # Increment view count
# # #                 cursor.execute("""
# # #                     UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
# # #                 """, (job_id,))
# # #                 connection.commit()
            
# # #             return job
# # #         except Exception as e:
# # #             print(f"❌ Error getting job by ID: {str(e)}")
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def search_jobs(filters):
# # #         """Search jobs with filters"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             query = """
# # #                 SELECT j.*, rp.company_name,
# # #                        CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
# # #                 FROM jobs j
# # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # #                 JOIN users u ON j.recruiter_id = u.id
# # #                 WHERE j.is_active = TRUE
# # #             """
# # #             params = []
            
# # #             if filters.get('search'):
# # #                 search_term = f'%{filters["search"]}%'
# # #                 query += """ AND (
# # #                     LOWER(j.title) LIKE LOWER(%s) OR 
# # #                     LOWER(j.description) LIKE LOWER(%s) OR 
# # #                     LOWER(j.requirements) LIKE LOWER(%s)
# # #                 )"""
# # #                 params.extend([search_term, search_term, search_term])
            
# # #             if filters.get('experience_level'):
# # #                 query += " AND j.experience_level = %s"
# # #                 params.append(filters['experience_level'])
            
# # #             if filters.get('min_pay'):
# # #                 try:
# # #                     min_pay = float(filters['min_pay'])
# # #                     query += " AND j.pay_per_hour >= %s"
# # #                     params.append(min_pay)
# # #                 except (ValueError, TypeError):
# # #                     pass
            
# # #             if filters.get('max_pay'):
# # #                 try:
# # #                     max_pay = float(filters['max_pay'])
# # #                     query += " AND j.pay_per_hour <= %s"
# # #                     params.append(max_pay)
# # #                 except (ValueError, TypeError):
# # #                     pass
            
# # #             if filters.get('job_type'):
# # #                 query += " AND j.job_type = %s"
# # #                 params.append(filters['job_type'])
            
# # #             if filters.get('is_remote'):
# # #                 query += " AND j.is_remote = TRUE"
            
# # #             query += " ORDER BY j.created_at DESC"
            
# # #             cursor.execute(query, params)
# # #             jobs = cursor.fetchall()
            
# # #             # Get skills and tech stack for each job
# # #             result = []
# # #             for job in jobs:
# # #                 cursor.execute("""
# # #                     SELECT s.name
# # #                     FROM job_skills js
# # #                     JOIN skills s ON js.skill_id = s.id
# # #                     WHERE js.job_id = %s
# # #                 """, (job['id'],))
# # #                 job['required_skills'] = [skill['name'] for skill in cursor.fetchall()]
                
# # #                 cursor.execute("""
# # #                     SELECT ts.name
# # #                     FROM job_tech_stacks jts
# # #                     JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# # #                     WHERE jts.job_id = %s
# # #                 """, (job['id'],))
# # #                 job['tech_stack'] = [tech['name'] for tech in cursor.fetchall()]
                
# # #                 result.append(job)
            
# # #             return result
# # #         except Exception as e:
# # #             print(f"❌ Error searching jobs: {str(e)}")
# # #             traceback.print_exc()
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_by_recruiter(recruiter_id):
# # #         """Get all jobs posted by a recruiter"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT j.*, 
# # #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as total_applications
# # #                 FROM jobs j
# # #                 WHERE j.recruiter_id = %s
# # #                 ORDER BY j.created_at DESC
# # #             """, (recruiter_id,))
            
# # #             jobs = cursor.fetchall()
# # #             return jobs
# # #         except Exception as e:
# # #             print(f"❌ Error getting jobs by recruiter: {str(e)}")
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()

# # # class JobApplication:
# # #     @staticmethod
# # #     def create(job_id, freelancer_id, application_data):
# # #         """Create a new job application"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             print(f"🔍 DEBUG - Starting application creation:")
# # #             print(f"   Job ID: {job_id}")
# # #             print(f"   Freelancer ID: {freelancer_id}")
# # #             print(f"   Application Data: {application_data}")
            
# # #             # Check if job exists
# # #             cursor.execute("SELECT id, title, recruiter_id FROM jobs WHERE id = %s", (job_id,))
# # #             job = cursor.fetchone()
# # #             if not job:
# # #                 print(f"❌ DEBUG: Job {job_id} not found")
# # #                 return None
# # #             print(f"✅ DEBUG: Job found: {job['title']}, Recruiter ID: {job['recruiter_id']}")
            
# # #             # Check if already applied
# # #             cursor.execute("""
# # #                 SELECT id, status FROM job_applications 
# # #                 WHERE job_id = %s AND freelancer_id = %s
# # #             """, (job_id, freelancer_id))
            
# # #             existing = cursor.fetchone()
            
# # #             if existing:
# # #                 print(f"⚠️ DEBUG: Found existing application ID: {existing['id']} with status: {existing['status']}")
# # #                 return None
# # #             else:
# # #                 print(f"✅ DEBUG: No existing application found")
            
# # #             # Get freelancer profile ID
# # #             cursor.execute("""
# # #                 SELECT id FROM freelancer_profiles WHERE user_id = %s
# # #             """, (freelancer_id,))
# # #             profile = cursor.fetchone()
            
# # #             if not profile:
# # #                 print(f"⚠️ DEBUG: Freelancer profile not found for user {freelancer_id}, creating one...")
# # #                 # Create profile automatically
# # #                 cursor.execute("""
# # #                     INSERT INTO freelancer_profiles (user_id, is_available, created_at, updated_at)
# # #                     VALUES (%s, TRUE, NOW(), NOW())
# # #                 """, (freelancer_id,))
# # #                 connection.commit()
                
# # #                 # Get the new profile ID
# # #                 cursor.execute("""
# # #                     SELECT id FROM freelancer_profiles WHERE user_id = %s
# # #                 """, (freelancer_id,))
# # #                 profile = cursor.fetchone()
# # #                 profile_id = profile['id']
# # #             else:
# # #                 profile_id = profile['id']
# # #                 print(f"✅ DEBUG: Found freelancer profile ID: {profile_id}")
            
# # #             # Handle proposed_rate - IMPORTANT FIX
# # #             proposed_rate = application_data.get('proposed_rate')
            
# # #             # Convert to appropriate value for database
# # #             if proposed_rate is None or proposed_rate == '':
# # #                 proposed_rate = None  # NULL in database
# # #                 print(f"📝 DEBUG: proposed_rate is empty, setting to NULL")
# # #             else:
# # #                 try:
# # #                     proposed_rate = float(proposed_rate)
# # #                     print(f"📝 DEBUG: proposed_rate converted to float: {proposed_rate}")
# # #                 except (ValueError, TypeError):
# # #                     proposed_rate = None
# # #                     print(f"⚠️ DEBUG: proposed_rate invalid, setting to NULL")
            
# # #             # Create application
# # #             cursor.execute("""
# # #                 INSERT INTO job_applications (
# # #                     job_id, freelancer_id, freelancer_profile_id,
# # #                     cover_letter, proposed_rate, applied_at
# # #                 ) VALUES (%s, %s, %s, %s, %s, NOW())
# # #             """, (
# # #                 job_id, freelancer_id, profile_id,
# # #                 application_data.get('cover_letter'),
# # #                 proposed_rate  # This will be None for empty values
# # #             ))
            
# # #             application_id = cursor.lastrowid
# # #             print(f"✅ DEBUG: Created application with ID: {application_id}")
            
# # #             # Update job applications count
# # #             cursor.execute("""
# # #                 UPDATE jobs SET applications_count = applications_count + 1
# # #                 WHERE id = %s
# # #             """, (job_id,))
            
# # #             connection.commit()
# # #             print(f"✅ Application {application_id} created for job {job_id}")
# # #             return application_id
            
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ DEBUG Error in JobApplication.create: {str(e)}")
# # #             traceback.print_exc()
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
                

    
# # #     @staticmethod
# # #     def update_status(application_id, status, recruiter_notes=None):
# # #         """Update application status"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             # Get application details
# # #             cursor.execute("""
# # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # #                        u.email as freelancer_email,
# # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # #                 FROM job_applications ja
# # #                 JOIN jobs j ON ja.job_id = j.id
# # #                 JOIN users u ON ja.freelancer_id = u.id
# # #                 WHERE ja.id = %s
# # #             """, (application_id,))
            
# # #             application = cursor.fetchone()
            
# # #             if not application:
# # #                 print(f"❌ Application {application_id} not found")
# # #                 return None
            
# # #             # Update status
# # #             cursor.execute("""
# # #                 UPDATE job_applications 
# # #                 SET status = %s, recruiter_notes = %s, updated_at = NOW()
# # #                 WHERE id = %s
# # #             """, (status, recruiter_notes, application_id))
            
# # #             connection.commit()
# # #             print(f"✅ Application {application_id} status updated to {status}")
            
# # #             # Fetch updated application
# # #             cursor.execute("""
# # #                 SELECT ja.*, j.title, j.recruiter_id, 
# # #                        u.email as freelancer_email,
# # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
# # #                 FROM job_applications ja
# # #                 JOIN jobs j ON ja.job_id = j.id
# # #                 JOIN users u ON ja.freelancer_id = u.id
# # #                 WHERE ja.id = %s
# # #             """, (application_id,))
# # #             return cursor.fetchone()
            
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ Error updating application status: {str(e)}")
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_by_job(job_id):
# # #         """Get all applications for a job"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT ja.*, 
# # #                        fp.hourly_rate, fp.years_of_experience,
# # #                        CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
# # #                        u.email as freelancer_email
# # #                 FROM job_applications ja
# # #                 JOIN users u ON ja.freelancer_id = u.id
# # #                 JOIN freelancer_profiles fp ON ja.freelancer_profile_id = fp.id
# # #                 WHERE ja.job_id = %s
# # #                 ORDER BY ja.applied_at DESC
# # #             """, (job_id,))
            
# # #             applications = cursor.fetchall()
            
# # #             # Get skills for each applicant
# # #             for app in applications:
# # #                 cursor.execute("""
# # #                     SELECT s.name
# # #                     FROM freelancer_skills fs
# # #                     JOIN skills s ON fs.skill_id = s.id
# # #                     WHERE fs.freelancer_profile_id = %s
# # #                 """, (app['freelancer_profile_id'],))
# # #                 app['skills'] = [skill['name'] for skill in cursor.fetchall()]
            
# # #             return applications
# # #         except Exception as e:
# # #             print(f"❌ Error getting applications by job: {str(e)}")
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_by_freelancer(freelancer_id):
# # #         """Get all applications by a freelancer"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
# # #                        rp.company_name
# # #                 FROM job_applications ja
# # #                 JOIN jobs j ON ja.job_id = j.id
# # #                 JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
# # #                 WHERE ja.freelancer_id = %s
# # #                 ORDER BY ja.applied_at DESC
# # #             """, (freelancer_id,))
            
# # #             applications = cursor.fetchall()
# # #             return applications
# # #         except Exception as e:
# # #             print(f"❌ Error getting applications by freelancer: {str(e)}")
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()


# # # class Notification:
# # #     @staticmethod
# # #     def create(user_id, title, message, notification_type='application', 
# # #                related_application_id=None, related_job_id=None):
# # #         """Create a new notification"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 INSERT INTO notifications (
# # #                     user_id, title, message, notification_type,
# # #                     related_application_id, related_job_id, created_at
# # #                 ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # #             """, (user_id, title, message, notification_type, 
# # #                   related_application_id, related_job_id))
            
# # #             notification_id = cursor.lastrowid
# # #             connection.commit()
# # #             print(f"✅ Notification {notification_id} created for user {user_id}")
# # #             return notification_id
# # #         except Exception as e:
# # #             if connection:
# # #                 connection.rollback()
# # #             print(f"❌ Error creating notification: {str(e)}")
# # #             return None
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_by_user(user_id, unread_only=False, limit=50):
# # #         """Get notifications for a user"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             query = """
# # #                 SELECT * FROM notifications 
# # #                 WHERE user_id = %s
# # #             """
# # #             params = [user_id]
            
# # #             if unread_only:
# # #                 query += " AND is_read = FALSE"
            
# # #             query += " ORDER BY created_at DESC LIMIT %s"
# # #             params.append(limit)
            
# # #             cursor.execute(query, params)
# # #             notifications = cursor.fetchall()
# # #             return notifications
# # #         except Exception as e:
# # #             print(f"❌ Error getting notifications: {str(e)}")
# # #             return []
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def mark_as_read(notification_id, user_id):
# # #         """Mark notification as read"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 UPDATE notifications 
# # #                 SET is_read = TRUE, read_at = NOW()
# # #                 WHERE id = %s AND user_id = %s
# # #             """, (notification_id, user_id))
            
# # #             affected = cursor.rowcount
# # #             connection.commit()
# # #             return affected > 0
# # #         except Exception as e:
# # #             print(f"❌ Error marking notification as read: {str(e)}")
# # #             return False
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def mark_all_as_read(user_id):
# # #         """Mark all notifications as read for a user"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 UPDATE notifications 
# # #                 SET is_read = TRUE, read_at = NOW()
# # #                 WHERE user_id = %s AND is_read = FALSE
# # #             """, (user_id,))
            
# # #             affected = cursor.rowcount
# # #             connection.commit()
# # #             return affected
# # #         except Exception as e:
# # #             print(f"❌ Error marking all notifications as read: {str(e)}")
# # #             return 0
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()
    
# # #     @staticmethod
# # #     def get_unread_count(user_id):
# # #         """Get unread notifications count"""
# # #         connection = None
# # #         cursor = None
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
            
# # #             cursor.execute("""
# # #                 SELECT COUNT(*) as count
# # #                 FROM notifications 
# # #                 WHERE user_id = %s AND is_read = FALSE
# # #             """, (user_id,))
            
# # #             result = cursor.fetchone()
# # #             return result['count'] if result else 0
# # #         except Exception as e:
# # #             print(f"❌ Error getting unread count: {str(e)}")
# # #             return 0
# # #         finally:
# # #             if cursor:
# # #                 cursor.close()
# # #             if connection:
# # #                 connection.close()


# # import json
# # import traceback
# # from datetime import datetime
# # from utils.auth_utils import hash_password, check_password
# # from database.db_config import get_db_connection as get_connection

# # # ==================== User Model ====================
# # class User:
# #     @staticmethod
# #     def create(username, email, password, first_name, last_name, user_type):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             password_hash = hash_password(password)
# #             cur.execute("""
# #                 INSERT INTO users (username, email, password_hash, first_name, last_name, user_type, date_joined)
# #                 VALUES (%s, %s, %s, %s, %s, %s, %s)
# #             """, (username, email, password_hash, first_name, last_name, user_type, datetime.now()))
# #             conn.commit()
# #             return cur.lastrowid
# #         except Exception as e:
# #             conn.rollback()
# #             print(f"Error creating user: {e}")
# #             traceback.print_exc()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def find_by_email(email):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT id, username, email, password_hash, first_name, last_name, user_type,
# #                        is_verified, date_joined
# #                 FROM users WHERE email = %s
# #             """, (email,))
# #             row = cur.fetchone()
# #             if row:
# #                 return {
# #                     'id': row['id'],
# #                     'username': row['username'],
# #                     'email': row['email'],
# #                     'password_hash': row['password_hash'],
# #                     'first_name': row['first_name'],
# #                     'last_name': row['last_name'],
# #                     'user_type': row['user_type'],
# #                     'is_verified': row['is_verified'],
# #                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
# #                 }
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def find_by_id(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT id, username, email, first_name, last_name, user_type,
# #                        is_verified, date_joined
# #                 FROM users WHERE id = %s
# #             """, (user_id,))
# #             row = cur.fetchone()
# #             if row:
# #                 return {
# #                     'id': row['id'],
# #                     'username': row['username'],
# #                     'email': row['email'],
# #                     'first_name': row['first_name'],
# #                     'last_name': row['last_name'],
# #                     'user_type': row['user_type'],
# #                     'is_verified': row['is_verified'],
# #                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
# #                 }
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def authenticate(email, password):
# #         user = User.find_by_email(email)
# #         if user and check_password(password, user['password_hash']):
# #             del user['password_hash']
# #             return user
# #         return None

# #     @staticmethod
# #     def verify_email(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 UPDATE users SET is_verified = TRUE, last_login = %s
# #                 WHERE id = %s
# #             """, (datetime.now(), user_id))
# #             conn.commit()
# #             return True
# #         except:
# #             conn.rollback()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# # # ==================== FreelancerProfile Model ====================
# # class FreelancerProfile:
# #     @staticmethod
# #     def get_by_user_id(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Fetch profile
# #             cur.execute("""
# #                 SELECT id, user_id, bio, hourly_rate, education, experience,
# #                        years_of_experience, github_url, linkedin_url, portfolio_url,
# #                        is_available, created_at, updated_at
# #                 FROM freelancer_profiles WHERE user_id = %s
# #             """, (user_id,))
# #             profile_row = cur.fetchone()
# #             if not profile_row:
# #                 return None

# #             profile = dict(profile_row)
# #             profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
# #             profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None

# #             # Fetch skills
# #             cur.execute("""
# #                 SELECT s.id, s.name, fs.proficiency_level
# #                 FROM freelancer_skills fs
# #                 JOIN skills s ON fs.skill_id = s.id
# #                 WHERE fs.freelancer_profile_id = %s
# #             """, (profile['id'],))
# #             skills = []
# #             for row in cur.fetchall():
# #                 skills.append({
# #                     'id': row['id'],
# #                     'name': row['name'],
# #                     'proficiency_level': row['proficiency_level']
# #                 })
# #             profile['skills'] = skills

# #             # Fetch tech stacks
# #             cur.execute("""
# #                 SELECT ts.id, ts.name, fts.experience_years
# #                 FROM freelancer_tech_stacks fts
# #                 JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
# #                 WHERE fts.freelancer_profile_id = %s
# #             """, (profile['id'],))
# #             tech_stacks = []
# #             for row in cur.fetchall():
# #                 tech_stacks.append({
# #                     'id': row['id'],
# #                     'name': row['name'],
# #                     'experience_years': row['experience_years']
# #                 })
# #             profile['tech_stacks'] = tech_stacks

# #             return profile
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def create_empty(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 INSERT INTO freelancer_profiles (user_id, company_name, created_at, updated_at)
# #                 VALUES (%s, %s,%s, %s)
# #             """, (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
# #             conn.commit()
# #             return FreelancerProfile.get_by_user_id(user_id)
# #         except:
# #             conn.rollback()
# #             print(f"Error creating empty recruiter profile: {e}")
# #             traceback.print_exc()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def update(user_id, data):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Get profile id
# #             cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (user_id,))
# #             profile_row = cur.fetchone()
# #             if not profile_row:
# #                 return False
# #             profile_id = profile_row['id']

# #             # Update profile fields
# #             fields = []
# #             values = []
# #             for key in ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience',
# #                         'github_url', 'linkedin_url', 'portfolio_url', 'is_available']:
# #                 if key in data:
# #                     fields.append(f"{key} = %s")
# #                     values.append(data[key])

# #             if fields:
# #                 values.append(datetime.now())
# #                 values.append(profile_id)
# #                 query = f"UPDATE freelancer_profiles SET {', '.join(fields)}, updated_at = %s WHERE id = %s"
# #                 cur.execute(query, tuple(values))

# #             # Update skills (replace all)
# #             if 'skills' in data:
# #                 # Delete existing
# #                 cur.execute("DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile_id,))
# #                 # Insert new
# #                 for skill in data['skills']:
# #                     # Ensure skill exists in skills table (or create)
# #                     if isinstance(skill, dict):
# #                         skill_name = skill.get('name')
# #                         proficiency = skill.get('proficiency_level', 'intermediate')
# #                     else:
# #                         skill_name = skill
# #                         proficiency = 'intermediate'
# #                     # Get or create skill
# #                     cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# #                     skill_row = cur.fetchone()
# #                     if skill_row:
# #                         skill_id = skill_row['id']
# #                     else:
# #                         cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# #                         skill_id = cur.lastrowid
# #                     cur.execute("""
# #                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
# #                         VALUES (%s, %s, %s)
# #                     """, (profile_id, skill_id, proficiency))

# #             # Update tech stacks
# #             if 'tech_stacks' in data:
# #                 cur.execute("DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s", (profile_id,))
# #                 for tech in data['tech_stacks']:
# #                     if isinstance(tech, dict):
# #                         tech_name = tech.get('name')
# #                         exp_years = tech.get('experience_years', 0)
# #                     else:
# #                         tech_name = tech
# #                         exp_years = 0
# #                     cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# #                     tech_row = cur.fetchone()
# #                     if tech_row:
# #                         tech_id = tech_row['id']
# #                     else:
# #                         cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# #                         tech_id = cur.lastrowid
# #                     cur.execute("""
# #                         INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
# #                         VALUES (%s, %s, %s)
# #                     """, (profile_id, tech_id, exp_years))

# #             conn.commit()
# #             return True
# #         except Exception as e:
# #             conn.rollback()
# #             print(f"Error updating freelancer profile: {e}")
# #             traceback.print_exc()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_stats(user_id):
# #         """Return dashboard stats for a freelancer"""
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Total applications
# #             cur.execute("SELECT COUNT(*) as count FROM job_applications WHERE freelancer_id = %s", (user_id,))
# #             total_applications = cur.fetchone()['count']

# #             # Pending applications (status = 'applied' or 'reviewed')
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM job_applications
# #                 WHERE freelancer_id = %s AND status IN ('applied', 'reviewed')
# #             """, (user_id,))
# #             pending_applications = cur.fetchone()['count']

# #             # Accepted applications
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM job_applications
# #                 WHERE freelancer_id = %s AND status = 'accepted'
# #             """, (user_id,))
# #             accepted_applications = cur.fetchone()['count']

# #             # Profile completion (count filled fields)
# #             cur.execute("SELECT * FROM freelancer_profiles WHERE user_id = %s", (user_id,))
# #             profile = cur.fetchone()
# #             completion = 0
# #             if profile:
# #                 fields = ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience']
# #                 filled = sum(1 for f in fields if profile.get(f))
# #                 # Also check if at least one skill exists
# #                 cur.execute("SELECT COUNT(*) as cnt FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile['id'],))
# #                 skill_count = cur.fetchone()['cnt']
# #                 if skill_count > 0:
# #                     filled += 1
# #                     fields.append('skills')
# #                 completion = int((filled / len(fields)) * 100) if fields else 0

# #             return {
# #                 'total_applications': total_applications,
# #                 'pending_applications': pending_applications,
# #                 'accepted_applications': accepted_applications,
# #                 'profile_completion': completion
# #             }
# #         finally:
# #             cur.close()
# #             conn.close()

# # # ==================== RecruiterProfile Model ====================
# # class RecruiterProfile:
# #     @staticmethod
# #     def get_by_user_id(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT id, user_id, company_name, company_website, company_size,
# #                        industry, company_description, location, phone, is_verified,
# #                        created_at, updated_at
# #                 FROM recruiter_profiles WHERE user_id = %s
# #             """, (user_id,))
# #             row = cur.fetchone()
# #             if row:
# #                 profile = dict(row)
# #                 profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
# #                 profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None
# #                 return profile
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def create_empty(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 INSERT INTO recruiter_profiles  (user_id, company_name, created_at, updated_at)
# #                 VALUES (%s, %s, %s, %s)
# #             """,  (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
# #             conn.commit()
# #             return RecruiterProfile.get_by_user_id(user_id)
# #         except:
# #             conn.rollback()
# #             print(f"Error creating empty recruiter profile: {e}")
# #             traceback.print_exc()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def update(user_id, data):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         fields = []
# #         values = []
# #         for key in ['company_name', 'company_website', 'company_size', 'industry',
# #                     'company_description', 'location', 'phone']:
# #             if key in data:
# #                 fields.append(f"{key} = %s")
# #                 values.append(data[key])

# #         if not fields:
# #             return False

# #         values.append(datetime.now())
# #         values.append(user_id)

# #         query = f"UPDATE recruiter_profiles SET {', '.join(fields)}, updated_at = %s WHERE user_id = %s"
# #         try:
# #             cur.execute(query, tuple(values))
# #             conn.commit()
# #             return cur.rowcount > 0
# #         except:
# #             conn.rollback()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_stats(user_id):
# #         """Return dashboard stats for a recruiter"""
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Total jobs posted
# #             cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s", (user_id,))
# #             total_jobs = cur.fetchone()['count']

# #             # Active jobs
# #             cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s AND is_active = TRUE", (user_id,))
# #             active_jobs = cur.fetchone()['count']

# #             # Total applications received
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 WHERE j.recruiter_id = %s
# #             """, (user_id,))
# #             total_applications = cur.fetchone()['count']

# #             # Pending applications (status = 'applied')
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 WHERE j.recruiter_id = %s AND ja.status = 'applied'
# #             """, (user_id,))
# #             pending_applications = cur.fetchone()['count']

# #             # Accepted applications
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 WHERE j.recruiter_id = %s AND ja.status = 'accepted'
# #             """, (user_id,))
# #             accepted_applications = cur.fetchone()['count']

# #             return {
# #                 'total_jobs': total_jobs,
# #                 'active_jobs': active_jobs,
# #                 'total_applications': total_applications,
# #                 'pending_applications': pending_applications,
# #                 'accepted_applications': accepted_applications
# #             }
# #         finally:
# #             cur.close()
# #             conn.close()

# # # ==================== Job Model ====================
# # class Job:
# #     @staticmethod
# #     def create(recruiter_id, data):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Get recruiter profile id
# #             cur.execute("SELECT id FROM recruiter_profiles WHERE user_id = %s", (recruiter_id,))
# #             profile_row = cur.fetchone()
# #             if not profile_row:
# #                 return None
# #             recruiter_profile_id = profile_row['id']

# #             cur.execute("""
# #                 INSERT INTO jobs (
# #                     recruiter_id, recruiter_profile_id, title, description,
# #                     pay_per_hour, experience_level, job_type, location, is_remote,
# #                     requirements, responsibilities, benefits, application_deadline,
# #                     is_active, created_at, updated_at
# #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# #             """, (
# #                 recruiter_id,
# #                 recruiter_profile_id,
# #                 data['title'],
# #                 data.get('description', ''),
# #                 data['pay_per_hour'],
# #                 data['experience_level'],
# #                 data.get('job_type', 'freelance'),
# #                 data.get('location', ''),
# #                 data.get('is_remote', True),
# #                 data.get('requirements', ''),
# #                 data.get('responsibilities', ''),
# #                 data.get('benefits', ''),
# #                 data.get('application_deadline'),
# #                 True,  # is_active
# #                 datetime.now(),
# #                 datetime.now()
# #             ))
# #             job_id = cur.lastrowid

# #             # Insert skills
# #             if 'required_skills' in data and data['required_skills']:
# #                 for skill_name in data['required_skills']:
# #                     # Get or create skill
# #                     cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
# #                     skill_row = cur.fetchone()
# #                     if skill_row:
# #                         skill_id = skill_row['id']
# #                     else:
# #                         cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
# #                         skill_id = cur.lastrowid
# #                     cur.execute("""
# #                         INSERT INTO job_skills (job_id, skill_id, is_required)
# #                         VALUES (%s, %s, %s)
# #                     """, (job_id, skill_id, True))

# #             # Insert tech stacks
# #             if 'tech_stack' in data and data['tech_stack']:
# #                 for tech_name in data['tech_stack']:
# #                     cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
# #                     tech_row = cur.fetchone()
# #                     if tech_row:
# #                         tech_id = tech_row['id']
# #                     else:
# #                         cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
# #                         tech_id = cur.lastrowid
# #                     cur.execute("""
# #                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
# #                         VALUES (%s, %s, %s)
# #                     """, (job_id, tech_id, True))

# #             conn.commit()
# #             return job_id
# #         except:
# #             conn.rollback()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_id(job_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT j.*, u.first_name, u.last_name, u.email,
# #                        rp.company_name
# #                 FROM jobs j
# #                 JOIN users u ON j.recruiter_id = u.id
# #                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
# #                 WHERE j.id = %s
# #             """, (job_id,))
# #             row = cur.fetchone()
# #             if not row:
# #                 return None
# #             job = dict(row)

# #             # Fetch skills
# #             cur.execute("""
# #                 SELECT s.id, s.name
# #                 FROM job_skills js
# #                 JOIN skills s ON js.skill_id = s.id
# #                 WHERE js.job_id = %s
# #             """, (job_id,))
# #             job['required_skills'] = [row['name'] for row in cur.fetchall()]

# #             # Fetch tech stacks
# #             cur.execute("""
# #                 SELECT ts.id, ts.name
# #                 FROM job_tech_stacks jts
# #                 JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
# #                 WHERE jts.job_id = %s
# #             """, (job_id,))
# #             job['tech_stack'] = [row['name'] for row in cur.fetchall()]

# #             return job
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_recruiter(recruiter_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT j.*,
# #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as applications_count
# #                 FROM jobs j
# #                 WHERE j.recruiter_id = %s
# #                 ORDER BY j.created_at DESC
# #             """, (recruiter_id,))
# #             rows = cur.fetchall()
# #             jobs = []
# #             for row in rows:
# #                 job = dict(row)
# #                 # Fetch skills and tech stacks for each (optional, can be done lazily)
# #                 jobs.append(job)
# #             return jobs
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_recent_by_recruiter(recruiter_id, limit=5):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT j.*,
# #                        (SELECT COUNT(*) FROM job_applications WHERE job_id = j.id) as applications_count
# #                 FROM jobs j
# #                 WHERE j.recruiter_id = %s
# #                 ORDER BY j.created_at DESC
# #                 LIMIT %s
# #             """, (recruiter_id, limit))
# #             rows = cur.fetchall()
# #             jobs = []
# #             for row in rows:
# #                 job = dict(row)
# #                 jobs.append(job)
# #             return jobs
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def search(filters):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         query = """
# #             SELECT j.*, u.first_name, u.last_name,
# #                    rp.company_name
# #             FROM jobs j
# #             JOIN users u ON j.recruiter_id = u.id
# #             LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
# #             WHERE j.is_active = TRUE
# #         """
# #         params = []
# #         if filters.get('search'):
# #             query += " AND (j.title LIKE %s OR j.description LIKE %s)"
# #             search_term = f"%{filters['search']}%"
# #             params.extend([search_term, search_term])
# #         if filters.get('experience_level'):
# #             query += " AND j.experience_level = %s"
# #             params.append(filters['experience_level'])
# #         if filters.get('min_pay'):
# #             query += " AND j.pay_per_hour >= %s"
# #             params.append(filters['min_pay'])
# #         if filters.get('max_pay'):
# #             query += " AND j.pay_per_hour <= %s"
# #             params.append(filters['max_pay'])
# #         if filters.get('job_type'):
# #             query += " AND j.job_type = %s"
# #             params.append(filters['job_type'])
# #         if filters.get('is_remote'):
# #             query += " AND j.is_remote = TRUE"
# #         query += " ORDER BY j.created_at DESC"

# #         try:
# #             cur.execute(query, params)
# #             rows = cur.fetchall()
# #             jobs = []
# #             for row in rows:
# #                 job = dict(row)
# #                 jobs.append(job)
# #             return jobs
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_recommended_for_freelancer(freelancer_id, limit=5):
# #         # Simple recommendation: newest active jobs
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT j.*, u.first_name, u.last_name,
# #                        rp.company_name
# #                 FROM jobs j
# #                 JOIN users u ON j.recruiter_id = u.id
# #                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
# #                 WHERE j.is_active = TRUE
# #                 ORDER BY j.created_at DESC
# #                 LIMIT %s
# #             """, (limit,))
# #             rows = cur.fetchall()
# #             jobs = []
# #             for row in rows:
# #                 job = dict(row)
# #                 jobs.append(job)
# #             return jobs
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def update(job_id, recruiter_id, data):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         fields = []
# #         values = []
# #         for key in ['title', 'description', 'requirements', 'responsibilities',
# #                     'pay_per_hour', 'experience_level', 'job_type', 'location', 'is_remote',
# #                     'benefits', 'application_deadline']:
# #             if key in data:
# #                 fields.append(f"{key} = %s")
# #                 values.append(data[key])

# #         if not fields:
# #             return False

# #         fields.append("updated_at = %s")
# #         values.append(datetime.now())
# #         values.append(job_id)
# #         values.append(recruiter_id)

# #         query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = %s AND recruiter_id = %s"
# #         try:
# #             cur.execute(query, tuple(values))
# #             conn.commit()
# #             return cur.rowcount > 0
# #         except:
# #             conn.rollback()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def toggle_active(job_id, recruiter_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 UPDATE jobs SET is_active = NOT is_active, updated_at = %s
# #                 WHERE id = %s AND recruiter_id = %s
# #             """, (datetime.now(), job_id, recruiter_id))
# #             conn.commit()
# #             # Return new status
# #             cur.execute("SELECT is_active FROM jobs WHERE id = %s", (job_id,))
# #             row = cur.fetchone()
# #             return row['is_active'] if row else None
# #         except:
# #             conn.rollback()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# # # ==================== JobApplication Model ====================
# # class JobApplication:
# #     @staticmethod
# #     def create(job_id, freelancer_id, application_data):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             # Check if already applied
# #             cur.execute("""
# #                 SELECT id FROM job_applications
# #                 WHERE job_id = %s AND freelancer_id = %s
# #             """, (job_id, freelancer_id))
# #             if cur.fetchone():
# #                 return None

# #             # Get freelancer profile id
# #             cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (freelancer_id,))
# #             profile_row = cur.fetchone()
# #             if not profile_row:
# #                 return None
# #             freelancer_profile_id = profile_row['id']

# #             cur.execute("""
# #                 INSERT INTO job_applications (
# #                     job_id, freelancer_id, freelancer_profile_id, cover_letter,
# #                     proposed_rate, availability_date, status, applied_at, updated_at
# #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# #             """, (
# #                 job_id,
# #                 freelancer_id,
# #                 freelancer_profile_id,
# #                 application_data.get('cover_letter', ''),
# #                 application_data.get('proposed_rate'),
# #                 application_data.get('availability_date'),
# #                 'applied',
# #                 datetime.now(),
# #                 datetime.now()
# #             ))
# #             app_id = cur.lastrowid
# #             conn.commit()
# #             return app_id
# #         except:
# #             conn.rollback()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_id(application_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT ja.*, 
# #                        j.title as job_title, 
# #                        j.recruiter_id,
# #                        u.first_name, 
# #                        u.last_name, 
# #                        u.email as freelancer_email,
# #                        fp.hourly_rate as freelancer_hourly_rate
# #                 FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 JOIN users u ON ja.freelancer_id = u.id
# #                 LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
# #                 WHERE ja.id = %s
# #             """, (application_id,))
# #             row = cur.fetchone()
# #             if row:
# #                 return dict(row)
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_freelancer(freelancer_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level, j.job_type,
# #                        u.first_name, u.last_name, rp.company_name
# #                 FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 JOIN users u ON j.recruiter_id = u.id
# #                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
# #                 WHERE ja.freelancer_id = %s
# #                 ORDER BY ja.applied_at DESC
# #             """, (freelancer_id,))
# #             rows = cur.fetchall()
# #             return [dict(row) for row in rows]
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_recent_by_freelancer(freelancer_id, limit=5):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
# #                        rp.company_name
# #                 FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 LEFT JOIN recruiter_profiles rp ON j.recruiter_id = rp.user_id
# #                 WHERE ja.freelancer_id = %s
# #                 ORDER BY ja.applied_at DESC
# #                 LIMIT %s
# #             """, (freelancer_id, limit))
# #             rows = cur.fetchall()
# #             return [dict(row) for row in rows]
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_job(job_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT ja.*, u.first_name, u.last_name, u.email as freelancer_email,
# #                        fp.hourly_rate
# #                 FROM job_applications ja
# #                 JOIN users u ON ja.freelancer_id = u.id
# #                 LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
# #                 WHERE ja.job_id = %s
# #                 ORDER BY ja.applied_at DESC
# #             """, (job_id,))
# #             rows = cur.fetchall()
# #             apps = []
# #             for row in rows:
# #                 app = dict(row)
# #                 # Fetch skills separately if needed
# #                 cur2 = conn.cursor()
# #                 cur2.execute("""
# #                     SELECT s.name
# #                     FROM freelancer_skills fs
# #                     JOIN skills s ON fs.skill_id = s.id
# #                     WHERE fs.freelancer_profile_id = (SELECT id FROM freelancer_profiles WHERE user_id = %s)
# #                 """, (app['freelancer_id'],))
# #                 app['skills'] = [r['name'] for r in cur2.fetchall()]
# #                 cur2.close()
# #                 apps.append(app)
# #             return apps
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_job_and_freelancer(job_id, freelancer_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT id FROM job_applications
# #                 WHERE job_id = %s AND freelancer_id = %s
# #             """, (job_id, freelancer_id))
# #             row = cur.fetchone()
# #             return row['id'] if row else None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_recent_for_recruiter(recruiter_id, limit=5):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT ja.*, j.title as job_title, u.first_name, u.last_name
# #                 FROM job_applications ja
# #                 JOIN jobs j ON ja.job_id = j.id
# #                 JOIN users u ON ja.freelancer_id = u.id
# #                 WHERE j.recruiter_id = %s
# #                 ORDER BY ja.applied_at DESC
# #                 LIMIT %s
# #             """, (recruiter_id, limit))
# #             rows = cur.fetchall()
# #             return [dict(row) for row in rows]
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def update_status(application_id, status, recruiter_notes=None):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             reviewed_at = None
# #             accepted_at = None
# #             rejected_at = None
# #             if status == 'reviewed':
# #                 reviewed_at = datetime.now()
# #             elif status == 'accepted':
# #                 accepted_at = datetime.now()
# #             elif status == 'rejected':
# #                 rejected_at = datetime.now()

# #             cur.execute("""
# #                 UPDATE job_applications
# #                 SET status = %s, recruiter_notes = %s, updated_at = %s,
# #                     reviewed_at = COALESCE(%s, reviewed_at),
# #                     accepted_at = COALESCE(%s, accepted_at),
# #                     rejected_at = COALESCE(%s, rejected_at)
# #                 WHERE id = %s
# #             """, (status, recruiter_notes, datetime.now(), reviewed_at, accepted_at, rejected_at, application_id))
# #             conn.commit()
# #             if cur.rowcount > 0:
# #                 return JobApplication.get_by_id(application_id)
# #             return None
# #         except:
# #             conn.rollback()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def withdraw(application_id, freelancer_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 DELETE FROM job_applications
# #                 WHERE id = %s AND freelancer_id = %s
# #             """, (application_id, freelancer_id))
# #             conn.commit()
# #             return cur.rowcount > 0
# #         except:
# #             conn.rollback()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# # # ==================== Notification Model ====================
# # class Notification:
# #     @staticmethod
# #     def create(user_id, title, message, notification_type,
# #                related_application_id=None, related_job_id=None):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 INSERT INTO notifications (
# #                     user_id, title, message, notification_type,
# #                     related_application_id, related_job_id,
# #                     is_read, created_at
# #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
# #             """, (
# #                 user_id, title, message, notification_type,
# #                 related_application_id, related_job_id,
# #                 False, datetime.now()
# #             ))
# #             conn.commit()
# #             return cur.lastrowid
# #         except:
# #             conn.rollback()
# #             return None
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_by_user(user_id, unread_only=False, limit=50):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             query = """
# #                 SELECT id, user_id, title, message, notification_type,
# #                        related_application_id, related_job_id, is_read, created_at
# #                 FROM notifications
# #                 WHERE user_id = %s
# #             """
# #             params = [user_id]
# #             if unread_only:
# #                 query += " AND is_read = FALSE"
# #             query += " ORDER BY created_at DESC LIMIT %s"
# #             params.append(limit)

# #             cur.execute(query, params)
# #             rows = cur.fetchall()
# #             notifs = []
# #             for row in rows:
# #                 notif = dict(row)
# #                 notif['created_at'] = notif['created_at'].isoformat() if notif['created_at'] else None
# #                 notifs.append(notif)
# #             return notifs
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def get_unread_count(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 SELECT COUNT(*) as count FROM notifications
# #                 WHERE user_id = %s AND is_read = FALSE
# #             """, (user_id,))
# #             return cur.fetchone()['count']
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def mark_as_read(notification_id, user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 UPDATE notifications SET is_read = TRUE, read_at = %s
# #                 WHERE id = %s AND user_id = %s
# #             """, (datetime.now(), notification_id, user_id))
# #             conn.commit()
# #             return cur.rowcount > 0
# #         except:
# #             conn.rollback()
# #             return False
# #         finally:
# #             cur.close()
# #             conn.close()

# #     @staticmethod
# #     def mark_all_as_read(user_id):
# #         conn = get_connection()
# #         cur = conn.cursor()
# #         try:
# #             cur.execute("""
# #                 UPDATE notifications SET is_read = TRUE, read_at = %s
# #                 WHERE user_id = %s AND is_read = FALSE
# #             """, (datetime.now(), user_id))
# #             conn.commit()
# #             return cur.rowcount
# #         except:
# #             conn.rollback()
# #             return 0
# #         finally:
# #             cur.close()
# #             conn.close()








# import json
# import traceback
# from datetime import datetime
# from utils.auth_utils import hash_password, check_password
# from database.db_config import get_db_connection as get_connection

# # ==================== User Model ====================
# class User:
#     @staticmethod
#     def create(username, email, password, first_name, last_name, user_type):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             password_hash = hash_password(password)
#             cur.execute("""
#                 INSERT INTO users (username, email, password_hash, first_name, last_name, user_type, date_joined)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """, (username, email, password_hash, first_name, last_name, user_type, datetime.now()))
#             conn.commit()
#             return cur.lastrowid
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating user: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def find_by_email(email):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id, username, email, password_hash, first_name, last_name, user_type,
#                        is_verified, date_joined
#                 FROM users WHERE email = %s
#             """, (email,))
#             row = cur.fetchone()
#             if row:
#                 return {
#                     'id': row['id'],
#                     'username': row['username'],
#                     'email': row['email'],
#                     'password_hash': row['password_hash'],
#                     'first_name': row['first_name'],
#                     'last_name': row['last_name'],
#                     'user_type': row['user_type'],
#                     'is_verified': row['is_verified'],
#                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
#                 }
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def find_by_id(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id, username, email, first_name, last_name, user_type,
#                        is_verified, date_joined
#                 FROM users WHERE id = %s
#             """, (user_id,))
#             row = cur.fetchone()
#             if row:
#                 return {
#                     'id': row['id'],
#                     'username': row['username'],
#                     'email': row['email'],
#                     'first_name': row['first_name'],
#                     'last_name': row['last_name'],
#                     'user_type': row['user_type'],
#                     'is_verified': row['is_verified'],
#                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
#                 }
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def authenticate(email, password):
#         user = User.find_by_email(email)
#         if user and check_password(password, user['password_hash']):
#             del user['password_hash']
#             return user
#         return None

#     @staticmethod
#     def verify_email(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 UPDATE users SET is_verified = TRUE, last_login = %s
#                 WHERE id = %s
#             """, (datetime.now(), user_id))
#             conn.commit()
#             return True
#         except:
#             conn.rollback()
#             return False
#         finally:
#             cur.close()
#             conn.close()

# # ==================== FreelancerProfile Model ====================
# class FreelancerProfile:
#     @staticmethod
#     def get_by_user_id(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Fetch profile
#             cur.execute("""
#                 SELECT id, user_id, bio, hourly_rate, education, experience,
#                        years_of_experience, github_url, linkedin_url, portfolio_url,
#                        is_available, created_at, updated_at
#                 FROM freelancer_profiles WHERE user_id = %s
#             """, (user_id,))
#             profile_row = cur.fetchone()
#             if not profile_row:
#                 return None

#             profile = dict(profile_row)
#             profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
#             profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None

#             # Fetch skills
#             cur.execute("""
#                 SELECT s.id, s.name, fs.proficiency_level
#                 FROM freelancer_skills fs
#                 JOIN skills s ON fs.skill_id = s.id
#                 WHERE fs.freelancer_profile_id = %s
#             """, (profile['id'],))
#             skills = []
#             for row in cur.fetchall():
#                 skills.append({
#                     'id': row['id'],
#                     'name': row['name'],
#                     'proficiency_level': row['proficiency_level']
#                 })
#             profile['skills'] = skills

#             # Fetch tech stacks
#             cur.execute("""
#                 SELECT ts.id, ts.name, fts.experience_years
#                 FROM freelancer_tech_stacks fts
#                 JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
#                 WHERE fts.freelancer_profile_id = %s
#             """, (profile['id'],))
#             tech_stacks = []
#             for row in cur.fetchall():
#                 tech_stacks.append({
#                     'id': row['id'],
#                     'name': row['name'],
#                     'experience_years': row['experience_years']
#                 })
#             profile['tech_stacks'] = tech_stacks

#             return profile
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def create_empty(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 INSERT INTO freelancer_profiles (user_id, company_name, created_at, updated_at)
#                 VALUES (%s, %s, %s, %s)
#             """, (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
#             conn.commit()
#             return FreelancerProfile.get_by_user_id(user_id)
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating empty freelancer profile: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def update(user_id, data):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Get profile id
#             cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (user_id,))
#             profile_row = cur.fetchone()
#             if not profile_row:
#                 return False
#             profile_id = profile_row['id']

#             # Update profile fields
#             fields = []
#             values = []
#             for key in ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience',
#                         'github_url', 'linkedin_url', 'portfolio_url', 'is_available']:
#                 if key in data:
#                     fields.append(f"{key} = %s")
#                     values.append(data[key])

#             if fields:
#                 values.append(datetime.now())
#                 values.append(profile_id)
#                 query = f"UPDATE freelancer_profiles SET {', '.join(fields)}, updated_at = %s WHERE id = %s"
#                 cur.execute(query, tuple(values))

#             # Update skills (replace all)
#             if 'skills' in data:
#                 # Delete existing
#                 cur.execute("DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile_id,))
#                 # Insert new
#                 for skill in data['skills']:
#                     # Ensure skill exists in skills table (or create)
#                     if isinstance(skill, dict):
#                         skill_name = skill.get('name')
#                         proficiency = skill.get('proficiency_level', 'intermediate')
#                     else:
#                         skill_name = skill
#                         proficiency = 'intermediate'
#                     # Get or create skill
#                     cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
#                     skill_row = cur.fetchone()
#                     if skill_row:
#                         skill_id = skill_row['id']
#                     else:
#                         cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
#                         skill_id = cur.lastrowid
#                     cur.execute("""
#                         INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
#                         VALUES (%s, %s, %s)
#                     """, (profile_id, skill_id, proficiency))

#             # Update tech stacks
#             if 'tech_stacks' in data:
#                 cur.execute("DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s", (profile_id,))
#                 for tech in data['tech_stacks']:
#                     if isinstance(tech, dict):
#                         tech_name = tech.get('name')
#                         exp_years = tech.get('experience_years', 0)
#                     else:
#                         tech_name = tech
#                         exp_years = 0
#                     cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
#                     tech_row = cur.fetchone()
#                     if tech_row:
#                         tech_id = tech_row['id']
#                     else:
#                         cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
#                         tech_id = cur.lastrowid
#                     cur.execute("""
#                         INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
#                         VALUES (%s, %s, %s)
#                     """, (profile_id, tech_id, exp_years))

#             conn.commit()
#             return True
#         except Exception as e:
#             conn.rollback()
#             print(f"Error updating freelancer profile: {e}")
#             traceback.print_exc()
#             return False
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_stats(user_id):
#         """Return dashboard stats for a freelancer"""
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Total applications
#             cur.execute("SELECT COUNT(*) as count FROM job_applications WHERE freelancer_id = %s", (user_id,))
#             total_applications = cur.fetchone()['count']

#             # Pending applications (status = 'applied' or 'reviewed')
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM job_applications
#                 WHERE freelancer_id = %s AND status IN ('applied', 'reviewed')
#             """, (user_id,))
#             pending_applications = cur.fetchone()['count']

#             # Accepted applications
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM job_applications
#                 WHERE freelancer_id = %s AND status = 'accepted'
#             """, (user_id,))
#             accepted_applications = cur.fetchone()['count']

#             # Profile completion (count filled fields)
#             cur.execute("SELECT * FROM freelancer_profiles WHERE user_id = %s", (user_id,))
#             profile = cur.fetchone()
#             completion = 0
#             if profile:
#                 fields = ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience']
#                 filled = sum(1 for f in fields if profile.get(f))
#                 # Also check if at least one skill exists
#                 cur.execute("SELECT COUNT(*) as cnt FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile['id'],))
#                 skill_count = cur.fetchone()['cnt']
#                 if skill_count > 0:
#                     filled += 1
#                     fields.append('skills')
#                 completion = int((filled / len(fields)) * 100) if fields else 0

#             return {
#                 'total_applications': total_applications,
#                 'pending_applications': pending_applications,
#                 'accepted_applications': accepted_applications,
#                 'profile_completion': completion
#             }
#         finally:
#             cur.close()
#             conn.close()

# # ==================== RecruiterProfile Model ====================
# class RecruiterProfile:
#     @staticmethod
#     def get_by_user_id(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id, user_id, company_name, company_website, company_size,
#                        industry, company_description, location, phone, is_verified,
#                        created_at, updated_at
#                 FROM recruiter_profiles WHERE user_id = %s
#             """, (user_id,))
#             row = cur.fetchone()
#             if row:
#                 profile = dict(row)
#                 profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
#                 profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None
#                 return profile
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def create_empty(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 INSERT INTO recruiter_profiles (user_id, company_name, created_at, updated_at)
#                 VALUES (%s, %s, %s, %s)
#             """, (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
#             conn.commit()
#             return RecruiterProfile.get_by_user_id(user_id)
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating empty recruiter profile: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def update(user_id, data):
#         conn = get_connection()
#         cur = conn.cursor()
#         fields = []
#         values = []
#         for key in ['company_name', 'company_website', 'company_size', 'industry',
#                     'company_description', 'location', 'phone']:
#             if key in data:
#                 fields.append(f"{key} = %s")
#                 values.append(data[key])

#         if not fields:
#             return False

#         values.append(datetime.now())
#         values.append(user_id)

#         query = f"UPDATE recruiter_profiles SET {', '.join(fields)}, updated_at = %s WHERE user_id = %s"
#         try:
#             cur.execute(query, tuple(values))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             conn.rollback()
#             print(f"Error updating recruiter profile: {e}")
#             return False
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_stats(user_id):
#         """Return dashboard stats for a recruiter"""
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Total jobs posted
#             cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s", (user_id,))
#             total_jobs = cur.fetchone()['count']

#             # Active jobs
#             cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s AND is_active = TRUE", (user_id,))
#             active_jobs = cur.fetchone()['count']

#             # Total applications received
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 WHERE j.recruiter_id = %s
#             """, (user_id,))
#             total_applications = cur.fetchone()['count']

#             # Pending applications (status = 'applied')
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 WHERE j.recruiter_id = %s AND ja.status = 'applied'
#             """, (user_id,))
#             pending_applications = cur.fetchone()['count']

#             # Accepted applications
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 WHERE j.recruiter_id = %s AND ja.status = 'accepted'
#             """, (user_id,))
#             accepted_applications = cur.fetchone()['count']

#             return {
#                 'total_jobs': total_jobs,
#                 'active_jobs': active_jobs,
#                 'total_applications': total_applications,
#                 'pending_applications': pending_applications,
#                 'accepted_applications': accepted_applications
#             }
#         finally:
#             cur.close()
#             conn.close()

# # ==================== Job Model ====================
# class Job:
#     @staticmethod
#     def create(recruiter_id, data):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Get recruiter profile id
#             cur.execute("SELECT id FROM recruiter_profiles WHERE user_id = %s", (recruiter_id,))
#             profile_row = cur.fetchone()
#             if not profile_row:
#                 return None
#             recruiter_profile_id = profile_row['id']

#             cur.execute("""
#                 INSERT INTO jobs (
#                     recruiter_id, recruiter_profile_id, title, description,
#                     pay_per_hour, experience_level, job_type, location, is_remote,
#                     requirements, responsibilities, benefits, application_deadline,
#                     is_active, created_at, updated_at
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 recruiter_id,
#                 recruiter_profile_id,
#                 data['title'],
#                 data.get('description', ''),
#                 data['pay_per_hour'],
#                 data['experience_level'],
#                 data.get('job_type', 'freelance'),
#                 data.get('location', ''),
#                 data.get('is_remote', True),
#                 data.get('requirements', ''),
#                 data.get('responsibilities', ''),
#                 data.get('benefits', ''),
#                 data.get('application_deadline'),
#                 True,  # is_active
#                 datetime.now(),
#                 datetime.now()
#             ))
#             job_id = cur.lastrowid

#             # Insert skills
#             if 'required_skills' in data and data['required_skills']:
#                 for skill_name in data['required_skills']:
#                     # Get or create skill
#                     cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
#                     skill_row = cur.fetchone()
#                     if skill_row:
#                         skill_id = skill_row['id']
#                     else:
#                         cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
#                         skill_id = cur.lastrowid
#                     cur.execute("""
#                         INSERT INTO job_skills (job_id, skill_id, is_required)
#                         VALUES (%s, %s, %s)
#                     """, (job_id, skill_id, True))

#             # Insert tech stacks
#             if 'tech_stack' in data and data['tech_stack']:
#                 for tech_name in data['tech_stack']:
#                     cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
#                     tech_row = cur.fetchone()
#                     if tech_row:
#                         tech_id = tech_row['id']
#                     else:
#                         cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
#                         tech_id = cur.lastrowid
#                     cur.execute("""
#                         INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
#                         VALUES (%s, %s, %s)
#                     """, (job_id, tech_id, True))

#             conn.commit()
#             return job_id
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating job: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_id(job_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT j.*, u.first_name, u.last_name, u.email,
#                        rp.company_name
#                 FROM jobs j
#                 JOIN users u ON j.recruiter_id = u.id
#                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
#                 WHERE j.id = %s
#             """, (job_id,))
#             row = cur.fetchone()
#             if not row:
#                 return None
#             job = dict(row)

#             # Fetch skills
#             cur.execute("""
#                 SELECT s.id, s.name
#                 FROM job_skills js
#                 JOIN skills s ON js.skill_id = s.id
#                 WHERE js.job_id = %s
#             """, (job_id,))
#             job['required_skills'] = [row['name'] for row in cur.fetchall()]

#             # Fetch tech stacks
#             cur.execute("""
#                 SELECT ts.id, ts.name
#                 FROM job_tech_stacks jts
#                 JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
#                 WHERE jts.job_id = %s
#             """, (job_id,))
#             job['tech_stack'] = [row['name'] for row in cur.fetchall()]

#             return job
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_recruiter(recruiter_id):
#         """Get all jobs posted by a recruiter, with applications_count directly from the column."""
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT j.*
#                 FROM jobs j
#                 WHERE j.recruiter_id = %s
#                 ORDER BY j.created_at DESC
#             """, (recruiter_id,))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         except Exception as e:
#             print(f"Error in get_by_recruiter: {e}")
#             traceback.print_exc()
#             return []
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_recent_by_recruiter(recruiter_id, limit=5):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT j.*
#                 FROM jobs j
#                 WHERE j.recruiter_id = %s
#                 ORDER BY j.created_at DESC
#                 LIMIT %s
#             """, (recruiter_id, limit))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         except Exception as e:
#             print(f"Error in get_recent_by_recruiter: {e}")
#             traceback.print_exc()
#             return []
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def search(filters):
#         conn = get_connection()
#         cur = conn.cursor()
#         query = """
#             SELECT j.*, u.first_name, u.last_name,
#                    rp.company_name
#             FROM jobs j
#             JOIN users u ON j.recruiter_id = u.id
#             LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
#             WHERE j.is_active = TRUE
#         """
#         params = []
#         if filters.get('search'):
#             query += " AND (j.title LIKE %s OR j.description LIKE %s)"
#             search_term = f"%{filters['search']}%"
#             params.extend([search_term, search_term])
#         if filters.get('experience_level'):
#             query += " AND j.experience_level = %s"
#             params.append(filters['experience_level'])
#         if filters.get('min_pay'):
#             query += " AND j.pay_per_hour >= %s"
#             params.append(filters['min_pay'])
#         if filters.get('max_pay'):
#             query += " AND j.pay_per_hour <= %s"
#             params.append(filters['max_pay'])
#         if filters.get('job_type'):
#             query += " AND j.job_type = %s"
#             params.append(filters['job_type'])
#         if filters.get('is_remote'):
#             query += " AND j.is_remote = TRUE"
#         query += " ORDER BY j.created_at DESC"

#         try:
#             cur.execute(query, params)
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_recommended_for_freelancer(freelancer_id, limit=5):
#         # Simple recommendation: newest active jobs
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT j.*, u.first_name, u.last_name,
#                        rp.company_name
#                 FROM jobs j
#                 JOIN users u ON j.recruiter_id = u.id
#                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
#                 WHERE j.is_active = TRUE
#                 ORDER BY j.created_at DESC
#                 LIMIT %s
#             """, (limit,))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def update(job_id, recruiter_id, data):
#         conn = get_connection()
#         cur = conn.cursor()
#         fields = []
#         values = []
#         for key in ['title', 'description', 'requirements', 'responsibilities',
#                     'pay_per_hour', 'experience_level', 'job_type', 'location', 'is_remote',
#                     'benefits', 'application_deadline']:
#             if key in data:
#                 fields.append(f"{key} = %s")
#                 values.append(data[key])

#         if not fields:
#             return False

#         fields.append("updated_at = %s")
#         values.append(datetime.now())
#         values.append(job_id)
#         values.append(recruiter_id)

#         query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = %s AND recruiter_id = %s"
#         try:
#             cur.execute(query, tuple(values))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             conn.rollback()
#             print(f"Error updating job: {e}")
#             return False
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def toggle_active(job_id, recruiter_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 UPDATE jobs SET is_active = NOT is_active, updated_at = %s
#                 WHERE id = %s AND recruiter_id = %s
#             """, (datetime.now(), job_id, recruiter_id))
#             conn.commit()
#             # Return new status
#             cur.execute("SELECT is_active FROM jobs WHERE id = %s", (job_id,))
#             row = cur.fetchone()
#             return row['is_active'] if row else None
#         except Exception as e:
#             conn.rollback()
#             print(f"Error toggling job active status: {e}")
#             return None
#         finally:
#             cur.close()
#             conn.close()

# # ==================== JobApplication Model ====================
# class JobApplication:
#     @staticmethod
#     def create(job_id, freelancer_id, application_data):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             # Check if already applied
#             cur.execute("""
#                 SELECT id FROM job_applications
#                 WHERE job_id = %s AND freelancer_id = %s
#             """, (job_id, freelancer_id))
#             if cur.fetchone():
#                 return None

#             # Get freelancer profile id
#             cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (freelancer_id,))
#             profile_row = cur.fetchone()
#             if not profile_row:
#                 return None
#             freelancer_profile_id = profile_row['id']

#             cur.execute("""
#                 INSERT INTO job_applications (
#                     job_id, freelancer_id, freelancer_profile_id, cover_letter,
#                     proposed_rate, availability_date, status, applied_at, updated_at
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 job_id,
#                 freelancer_id,
#                 freelancer_profile_id,
#                 application_data.get('cover_letter', ''),
#                 application_data.get('proposed_rate'),
#                 application_data.get('availability_date'),
#                 'applied',
#                 datetime.now(),
#                 datetime.now()
#             ))
#             app_id = cur.lastrowid

#             # ✅ Update the job's applications_count
#             cur.execute("UPDATE jobs SET applications_count = applications_count + 1 WHERE id = %s", (job_id,))

#             conn.commit()
#             return app_id
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating job application: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_id(application_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT ja.*, 
#                        j.title as job_title, 
#                        j.recruiter_id,
#                        u.first_name, 
#                        u.last_name, 
#                        u.email as freelancer_email,
#                        fp.hourly_rate as freelancer_hourly_rate
#                 FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 JOIN users u ON ja.freelancer_id = u.id
#                 LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
#                 WHERE ja.id = %s
#             """, (application_id,))
#             row = cur.fetchone()
#             if row:
#                 return dict(row)
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_freelancer(freelancer_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level, j.job_type,
#                        u.first_name, u.last_name, rp.company_name
#                 FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 JOIN users u ON j.recruiter_id = u.id
#                 LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
#                 WHERE ja.freelancer_id = %s
#                 ORDER BY ja.applied_at DESC
#             """, (freelancer_id,))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_recent_by_freelancer(freelancer_id, limit=5):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
#                        rp.company_name
#                 FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 LEFT JOIN recruiter_profiles rp ON j.recruiter_id = rp.user_id
#                 WHERE ja.freelancer_id = %s
#                 ORDER BY ja.applied_at DESC
#                 LIMIT %s
#             """, (freelancer_id, limit))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_job(job_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT ja.*, u.first_name, u.last_name, u.email as freelancer_email,
#                        fp.hourly_rate
#                 FROM job_applications ja
#                 JOIN users u ON ja.freelancer_id = u.id
#                 LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
#                 WHERE ja.job_id = %s
#                 ORDER BY ja.applied_at DESC
#             """, (job_id,))
#             rows = cur.fetchall()
#             apps = []
#             for row in rows:
#                 app = dict(row)
#                 # Fetch skills separately if needed
#                 cur2 = conn.cursor()
#                 cur2.execute("""
#                     SELECT s.name
#                     FROM freelancer_skills fs
#                     JOIN skills s ON fs.skill_id = s.id
#                     WHERE fs.freelancer_profile_id = (SELECT id FROM freelancer_profiles WHERE user_id = %s)
#                 """, (app['freelancer_id'],))
#                 app['skills'] = [r['name'] for r in cur2.fetchall()]
#                 cur2.close()
#                 apps.append(app)
#             return apps
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_job_and_freelancer(job_id, freelancer_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id FROM job_applications
#                 WHERE job_id = %s AND freelancer_id = %s
#             """, (job_id, freelancer_id))
#             row = cur.fetchone()
#             return row['id'] if row else None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_recent_for_recruiter(recruiter_id, limit=5):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT ja.*, j.title as job_title, u.first_name, u.last_name
#                 FROM job_applications ja
#                 JOIN jobs j ON ja.job_id = j.id
#                 JOIN users u ON ja.freelancer_id = u.id
#                 WHERE j.recruiter_id = %s
#                 ORDER BY ja.applied_at DESC
#                 LIMIT %s
#             """, (recruiter_id, limit))
#             rows = cur.fetchall()
#             return [dict(row) for row in rows]
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def update_status(application_id, status, recruiter_notes=None):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             reviewed_at = None
#             accepted_at = None
#             rejected_at = None
#             if status == 'reviewed':
#                 reviewed_at = datetime.now()
#             elif status == 'accepted':
#                 accepted_at = datetime.now()
#             elif status == 'rejected':
#                 rejected_at = datetime.now()

#             cur.execute("""
#                 UPDATE job_applications
#                 SET status = %s, recruiter_notes = %s, updated_at = %s,
#                     reviewed_at = COALESCE(%s, reviewed_at),
#                     accepted_at = COALESCE(%s, accepted_at),
#                     rejected_at = COALESCE(%s, rejected_at)
#                 WHERE id = %s
#             """, (status, recruiter_notes, datetime.now(), reviewed_at, accepted_at, rejected_at, application_id))
#             conn.commit()
#             if cur.rowcount > 0:
#                 return JobApplication.get_by_id(application_id)
#             return None
#         except Exception as e:
#             conn.rollback()
#             print(f"Error updating application status: {e}")
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def withdraw(application_id, freelancer_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 DELETE FROM job_applications
#                 WHERE id = %s AND freelancer_id = %s
#             """, (application_id, freelancer_id))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             conn.rollback()
#             print(f"Error withdrawing application: {e}")
#             return False
#         finally:
#             cur.close()
#             conn.close()

# # ==================== Notification Model ====================
# class Notification:
#     @staticmethod
#     def create(user_id, title, message, notification_type,
#                related_application_id=None, related_job_id=None):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 INSERT INTO notifications (
#                     user_id, title, message, notification_type,
#                     related_application_id, related_job_id,
#                     is_read, created_at
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 user_id, title, message, notification_type,
#                 related_application_id, related_job_id,
#                 False, datetime.now()
#             ))
#             conn.commit()
#             return cur.lastrowid
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating notification: {e}")
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_by_user(user_id, unread_only=False, limit=50):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             query = """
#                 SELECT id, user_id, title, message, notification_type,
#                        related_application_id, related_job_id, is_read, created_at
#                 FROM notifications
#                 WHERE user_id = %s
#             """
#             params = [user_id]
#             if unread_only:
#                 query += " AND is_read = FALSE"
#             query += " ORDER BY created_at DESC LIMIT %s"
#             params.append(limit)

#             cur.execute(query, params)
#             rows = cur.fetchall()
#             notifs = []
#             for row in rows:
#                 notif = dict(row)
#                 notif['created_at'] = notif['created_at'].isoformat() if notif['created_at'] else None
#                 notifs.append(notif)
#             return notifs
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def get_unread_count(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT COUNT(*) as count FROM notifications
#                 WHERE user_id = %s AND is_read = FALSE
#             """, (user_id,))
#             return cur.fetchone()['count']
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def mark_as_read(notification_id, user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 UPDATE notifications SET is_read = TRUE, read_at = %s
#                 WHERE id = %s AND user_id = %s
#             """, (datetime.now(), notification_id, user_id))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             conn.rollback()
#             print(f"Error marking notification as read: {e}")
#             return False
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def mark_all_as_read(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 UPDATE notifications SET is_read = TRUE, read_at = %s
#                 WHERE user_id = %s AND is_read = FALSE
#             """, (datetime.now(), user_id))
#             conn.commit()
#             return cur.rowcount
#         except Exception as e:
#             conn.rollback()
#             print(f"Error marking all notifications as read: {e}")
#             return 0
#         finally:
#             cur.close()
#             conn.close()





import json
import traceback
from datetime import datetime
from utils.auth_utils import hash_password, check_password
from database.db_config import get_db_connection as get_connection

# ==================== User Model ====================
# class User:
#     @staticmethod
#     def create(username, email, password, first_name, last_name, user_type):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             password_hash = hash_password(password)
#             cur.execute("""
#                 INSERT INTO users (username, email, password_hash, first_name, last_name, user_type, date_joined)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """, (username, email, password_hash, first_name, last_name, user_type, datetime.now()))
#             conn.commit()
#             return cur.lastrowid
#         except Exception as e:
#             conn.rollback()
#             print(f"Error creating user: {e}")
#             traceback.print_exc()
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def find_by_email(email):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id, username, email, password_hash, first_name, last_name, user_type,
#                        is_verified, date_joined
#                 FROM users WHERE email = %s
#             """, (email,))
#             row = cur.fetchone()
#             if row:
#                 return {
#                     'id': row['id'],
#                     'username': row['username'],
#                     'email': row['email'],
#                     'password_hash': row['password_hash'],
#                     'first_name': row['first_name'],
#                     'last_name': row['last_name'],
#                     'user_type': row['user_type'],
#                     'is_verified': row['is_verified'],
#                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
#                 }
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def find_by_id(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 SELECT id, username, email, first_name, last_name, user_type,
#                        is_verified, date_joined
#                 FROM users WHERE id = %s
#             """, (user_id,))
#             row = cur.fetchone()
#             if row:
#                 return {
#                     'id': row['id'],
#                     'username': row['username'],
#                     'email': row['email'],
#                     'first_name': row['first_name'],
#                     'last_name': row['last_name'],
#                     'user_type': row['user_type'],
#                     'is_verified': row['is_verified'],
#                     'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
#                 }
#             return None
#         finally:
#             cur.close()
#             conn.close()

#     @staticmethod
#     def authenticate(email, password):
#         user = User.find_by_email(email)
#         if user and check_password(password, user['password_hash']):
#             del user['password_hash']
#             return user
#         return None

#     @staticmethod
#     def verify_email(user_id):
#         conn = get_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute("""
#                 UPDATE users SET is_verified = TRUE, last_login = %s
#                 WHERE id = %s
#             """, (datetime.now(), user_id))
#             conn.commit()
#             return True
#         except:
#             conn.rollback()
#             return False
#         finally:
#             cur.close()
#             conn.close()
# ==================== User Model ====================
class User:
    @staticmethod
    def create(username, email, password, first_name, last_name, user_type):
        conn = get_connection()
        cur = conn.cursor()
        try:
            password_hash = hash_password(password)
            cur.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, email, password_hash, first_name, last_name, user_type, datetime.now()))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"Error creating user: {e}")
            traceback.print_exc()
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def find_by_email(email):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, username, email, password_hash, first_name, last_name, user_type,
                       is_verified, date_joined
                FROM users WHERE email = %s
            """, (email,))
            row = cur.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'password_hash': row['password_hash'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'user_type': row['user_type'],
                    'is_verified': row['is_verified'],
                    'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
                }
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def find_by_id(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, username, email, first_name, last_name, user_type,
                       is_verified, date_joined
                FROM users WHERE id = %s
            """, (user_id,))
            row = cur.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'user_type': row['user_type'],
                    'is_verified': row['is_verified'],
                    'date_joined': row['date_joined'].isoformat() if row['date_joined'] else None
                }
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def authenticate(email, password):
        user = User.find_by_email(email)
        if user and check_password(password, user['password_hash']):
            del user['password_hash']
            return user
        return None

    @staticmethod
    def verify_email(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE users SET is_verified = TRUE, last_login = %s
                WHERE id = %s
            """, (datetime.now(), user_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def set_verification_token(user_id, token):
        """Store verification token in database (optional)"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE users SET verification_token = %s WHERE id = %s", (token, user_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error storing verification token: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# ==================== FreelancerProfile Model ====================
class FreelancerProfile:
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, user_id, bio, hourly_rate, education, experience,
                       years_of_experience, github_url, linkedin_url, portfolio_url,
                       is_available, created_at, updated_at
                FROM freelancer_profiles WHERE user_id = %s
            """, (user_id,))
            profile_row = cur.fetchone()
            if not profile_row:
                return None

            profile = dict(profile_row)
            profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
            profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None

            # Fetch skills
            cur.execute("""
                SELECT s.id, s.name, fs.proficiency_level
                FROM freelancer_skills fs
                JOIN skills s ON fs.skill_id = s.id
                WHERE fs.freelancer_profile_id = %s
            """, (profile['id'],))
            skills = []
            for row in cur.fetchall():
                skills.append({
                    'id': row['id'],
                    'name': row['name'],
                    'proficiency_level': row['proficiency_level']
                })
            profile['skills'] = skills

            # Fetch tech stacks
            cur.execute("""
                SELECT ts.id, ts.name, fts.experience_years
                FROM freelancer_tech_stacks fts
                JOIN tech_stacks ts ON fts.tech_stack_id = ts.id
                WHERE fts.freelancer_profile_id = %s
            """, (profile['id'],))
            tech_stacks = []
            for row in cur.fetchall():
                tech_stacks.append({
                    'id': row['id'],
                    'name': row['name'],
                    'experience_years': row['experience_years']
                })
            profile['tech_stacks'] = tech_stacks

            return profile
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def create_empty(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO freelancer_profiles (user_id, company_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
            conn.commit()
            return FreelancerProfile.get_by_user_id(user_id)
        except Exception as e:
            conn.rollback()
            print(f"Error creating empty freelancer profile: {e}")
            traceback.print_exc()
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update(user_id, data):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Get profile id
            cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (user_id,))
            profile_row = cur.fetchone()
            if not profile_row:
                return False
            profile_id = profile_row['id']

            # Update profile fields
            fields = []
            values = []
            for key in ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience',
                        'github_url', 'linkedin_url', 'portfolio_url', 'is_available']:
                if key in data:
                    fields.append(f"{key} = %s")
                    values.append(data[key])

            if fields:
                values.append(datetime.now())
                values.append(profile_id)
                query = f"UPDATE freelancer_profiles SET {', '.join(fields)}, updated_at = %s WHERE id = %s"
                cur.execute(query, tuple(values))

            # Update skills (replace all)
            if 'skills' in data:
                # Delete existing
                cur.execute("DELETE FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile_id,))
                # Insert new
                for skill in data['skills']:
                    if isinstance(skill, dict):
                        skill_name = skill.get('name')
                        proficiency = skill.get('proficiency_level', 'intermediate')
                    else:
                        skill_name = skill
                        proficiency = 'intermediate'
                    # Get or create skill
                    cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
                    skill_row = cur.fetchone()
                    if skill_row:
                        skill_id = skill_row['id']
                    else:
                        cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
                        skill_id = cur.lastrowid
                    cur.execute("""
                        INSERT INTO freelancer_skills (freelancer_profile_id, skill_id, proficiency_level)
                        VALUES (%s, %s, %s)
                    """, (profile_id, skill_id, proficiency))

            # Update tech stacks
            if 'tech_stacks' in data:
                cur.execute("DELETE FROM freelancer_tech_stacks WHERE freelancer_profile_id = %s", (profile_id,))
                for tech in data['tech_stacks']:
                    if isinstance(tech, dict):
                        tech_name = tech.get('name')
                        exp_years = tech.get('experience_years', 0)
                    else:
                        tech_name = tech
                        exp_years = 0
                    cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
                    tech_row = cur.fetchone()
                    if tech_row:
                        tech_id = tech_row['id']
                    else:
                        cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
                        tech_id = cur.lastrowid
                    cur.execute("""
                        INSERT INTO freelancer_tech_stacks (freelancer_profile_id, tech_stack_id, experience_years)
                        VALUES (%s, %s, %s)
                    """, (profile_id, tech_id, exp_years))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating freelancer profile: {e}")
            traceback.print_exc()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_stats(user_id):
        """Return dashboard stats for a freelancer"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Total applications
            cur.execute("SELECT COUNT(*) as count FROM job_applications WHERE freelancer_id = %s", (user_id,))
            total_applications = cur.fetchone()['count']

            # Pending applications (status = 'applied' or 'reviewed')
            cur.execute("""
                SELECT COUNT(*) as count FROM job_applications
                WHERE freelancer_id = %s AND status IN ('applied', 'reviewed')
            """, (user_id,))
            pending_applications = cur.fetchone()['count']

            # Accepted applications
            cur.execute("""
                SELECT COUNT(*) as count FROM job_applications
                WHERE freelancer_id = %s AND status = 'accepted'
            """, (user_id,))
            accepted_applications = cur.fetchone()['count']

            # Profile completion (count filled fields)
            cur.execute("SELECT * FROM freelancer_profiles WHERE user_id = %s", (user_id,))
            profile = cur.fetchone()
            completion = 0
            if profile:
                fields = ['bio', 'hourly_rate', 'education', 'experience', 'years_of_experience']
                filled = sum(1 for f in fields if profile.get(f))
                # Also check if at least one skill exists
                cur.execute("SELECT COUNT(*) as cnt FROM freelancer_skills WHERE freelancer_profile_id = %s", (profile['id'],))
                skill_count = cur.fetchone()['cnt']
                if skill_count > 0:
                    filled += 1
                    fields.append('skills')
                completion = int((filled / len(fields)) * 100) if fields else 0

            return {
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications,
                'profile_completion': completion
            }
        finally:
            cur.close()
            conn.close()

# ==================== RecruiterProfile Model ====================
class RecruiterProfile:
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, user_id, company_name, company_website, company_size,
                       industry, company_description, location, phone, is_verified,
                       created_at, updated_at
                FROM recruiter_profiles WHERE user_id = %s
            """, (user_id,))
            row = cur.fetchone()
            if row:
                profile = dict(row)
                profile['created_at'] = profile['created_at'].isoformat() if profile['created_at'] else None
                profile['updated_at'] = profile['updated_at'].isoformat() if profile['updated_at'] else None
                return profile
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def create_empty(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO recruiter_profiles (user_id, company_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, f"Company of user {user_id}", datetime.now(), datetime.now()))
            conn.commit()
            return RecruiterProfile.get_by_user_id(user_id)
        except Exception as e:
            conn.rollback()
            print(f"Error creating empty recruiter profile: {e}")
            traceback.print_exc()
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update(user_id, data):
        conn = get_connection()
        cur = conn.cursor()
        fields = []
        values = []
        for key in ['company_name', 'company_website', 'company_size', 'industry',
                    'company_description', 'location', 'phone']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])

        if not fields:
            return False

        values.append(datetime.now())
        values.append(user_id)

        query = f"UPDATE recruiter_profiles SET {', '.join(fields)}, updated_at = %s WHERE user_id = %s"
        try:
            cur.execute(query, tuple(values))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating recruiter profile: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_stats(user_id):
        """Return dashboard stats for a recruiter"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Total jobs posted
            cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s", (user_id,))
            total_jobs = cur.fetchone()['count']

            # Active jobs
            cur.execute("SELECT COUNT(*) as count FROM jobs WHERE recruiter_id = %s AND is_active = TRUE", (user_id,))
            active_jobs = cur.fetchone()['count']

            # Total applications received
            cur.execute("""
                SELECT COUNT(*) as count FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                WHERE j.recruiter_id = %s
            """, (user_id,))
            total_applications = cur.fetchone()['count']

            # Pending applications (status = 'applied')
            cur.execute("""
                SELECT COUNT(*) as count FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                WHERE j.recruiter_id = %s AND ja.status = 'applied'
            """, (user_id,))
            pending_applications = cur.fetchone()['count']

            # Accepted applications
            cur.execute("""
                SELECT COUNT(*) as count FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                WHERE j.recruiter_id = %s AND ja.status = 'accepted'
            """, (user_id,))
            accepted_applications = cur.fetchone()['count']

            return {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications
            }
        finally:
            cur.close()
            conn.close()

# ==================== Job Model ====================
class Job:
    @staticmethod
    def create(recruiter_id, data):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Get recruiter profile id
            cur.execute("SELECT id FROM recruiter_profiles WHERE user_id = %s", (recruiter_id,))
            profile_row = cur.fetchone()
            if not profile_row:
                return None
            recruiter_profile_id = profile_row['id']

            cur.execute("""
                INSERT INTO jobs (
                    recruiter_id, recruiter_profile_id, title, description,
                    pay_per_hour, experience_level, job_type, location, is_remote,
                    requirements, responsibilities, benefits, application_deadline,
                    is_active, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                recruiter_id,
                recruiter_profile_id,
                data['title'],
                data.get('description', ''),
                data['pay_per_hour'],
                data['experience_level'],
                data.get('job_type', 'freelance'),
                data.get('location', ''),
                data.get('is_remote', True),
                data.get('requirements', ''),
                data.get('responsibilities', ''),
                data.get('benefits', ''),
                data.get('application_deadline'),
                True,
                datetime.now(),
                datetime.now()
            ))
            job_id = cur.lastrowid

            # Insert skills
            if 'required_skills' in data and data['required_skills']:
                for skill_name in data['required_skills']:
                    cur.execute("SELECT id FROM skills WHERE name = %s", (skill_name,))
                    skill_row = cur.fetchone()
                    if skill_row:
                        skill_id = skill_row['id']
                    else:
                        cur.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
                        skill_id = cur.lastrowid
                    cur.execute("""
                        INSERT INTO job_skills (job_id, skill_id, is_required)
                        VALUES (%s, %s, %s)
                    """, (job_id, skill_id, True))

            # Insert tech stacks
            if 'tech_stack' in data and data['tech_stack']:
                for tech_name in data['tech_stack']:
                    cur.execute("SELECT id FROM tech_stacks WHERE name = %s", (tech_name,))
                    tech_row = cur.fetchone()
                    if tech_row:
                        tech_id = tech_row['id']
                    else:
                        cur.execute("INSERT INTO tech_stacks (name) VALUES (%s)", (tech_name,))
                        tech_id = cur.lastrowid
                    cur.execute("""
                        INSERT INTO job_tech_stacks (job_id, tech_stack_id, is_required)
                        VALUES (%s, %s, %s)
                    """, (job_id, tech_id, True))

            conn.commit()
            return job_id
        except Exception as e:
            conn.rollback()
            print(f"Error creating job: {e}")
            traceback.print_exc()
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(job_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT j.*, u.first_name, u.last_name, u.email,
                       rp.company_name
                FROM jobs j
                JOIN users u ON j.recruiter_id = u.id
                LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
                WHERE j.id = %s
            """, (job_id,))
            row = cur.fetchone()
            if not row:
                return None
            job = dict(row)

            # Fetch skills
            cur.execute("""
                SELECT s.id, s.name
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.id
                WHERE js.job_id = %s
            """, (job_id,))
            job['required_skills'] = [r['name'] for r in cur.fetchall()]

            # Fetch tech stacks
            cur.execute("""
                SELECT ts.id, ts.name
                FROM job_tech_stacks jts
                JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
                WHERE jts.job_id = %s
            """, (job_id,))
            job['tech_stack'] = [r['name'] for r in cur.fetchall()]

            return job
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_recruiter(recruiter_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT j.*
                FROM jobs j
                WHERE j.recruiter_id = %s
                ORDER BY j.created_at DESC
            """, (recruiter_id,))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error in get_by_recruiter: {e}")
            traceback.print_exc()
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_recent_by_recruiter(recruiter_id, limit=5):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT j.*
                FROM jobs j
                WHERE j.recruiter_id = %s
                ORDER BY j.created_at DESC
                LIMIT %s
            """, (recruiter_id, limit))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error in get_recent_by_recruiter: {e}")
            traceback.print_exc()
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def search(filters):
        conn = get_connection()
        cur = conn.cursor()
        query = """
            SELECT j.*, u.first_name, u.last_name,
                   rp.company_name
            FROM jobs j
            JOIN users u ON j.recruiter_id = u.id
            LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
            WHERE j.is_active = TRUE
        """
        params = []
        if filters.get('search'):
            query += " AND (j.title LIKE %s OR j.description LIKE %s)"
            search_term = f"%{filters['search']}%"
            params.extend([search_term, search_term])
        if filters.get('experience_level'):
            query += " AND j.experience_level = %s"
            params.append(filters['experience_level'])
        if filters.get('min_pay'):
            query += " AND j.pay_per_hour >= %s"
            params.append(filters['min_pay'])
        if filters.get('max_pay'):
            query += " AND j.pay_per_hour <= %s"
            params.append(filters['max_pay'])
        if filters.get('job_type'):
            query += " AND j.job_type = %s"
            params.append(filters['job_type'])
        if filters.get('is_remote'):
            query += " AND j.is_remote = TRUE"
        query += " ORDER BY j.created_at DESC"

        try:
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_recommended_for_freelancer(freelancer_id, limit=5):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT j.*, u.first_name, u.last_name,
                       rp.company_name
                FROM jobs j
                JOIN users u ON j.recruiter_id = u.id
                LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
                WHERE j.is_active = TRUE
                ORDER BY j.created_at DESC
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update(job_id, recruiter_id, data):
        conn = get_connection()
        cur = conn.cursor()
        fields = []
        values = []
        for key in ['title', 'description', 'requirements', 'responsibilities',
                    'pay_per_hour', 'experience_level', 'job_type', 'location', 'is_remote',
                    'benefits', 'application_deadline']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])

        if not fields:
            return False

        fields.append("updated_at = %s")
        values.append(datetime.now())
        values.append(job_id)
        values.append(recruiter_id)

        query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = %s AND recruiter_id = %s"
        try:
            cur.execute(query, tuple(values))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating job: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def toggle_active(job_id, recruiter_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE jobs SET is_active = NOT is_active, updated_at = %s
                WHERE id = %s AND recruiter_id = %s
            """, (datetime.now(), job_id, recruiter_id))
            conn.commit()
            cur.execute("SELECT is_active FROM jobs WHERE id = %s", (job_id,))
            row = cur.fetchone()
            return row['is_active'] if row else None
        except Exception as e:
            conn.rollback()
            print(f"Error toggling job active status: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete(job_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting job: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# ==================== JobApplication Model ====================
class JobApplication:
    @staticmethod
    def create(job_id, freelancer_id, application_data):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Check if already applied
            cur.execute("""
                SELECT id FROM job_applications
                WHERE job_id = %s AND freelancer_id = %s
            """, (job_id, freelancer_id))
            if cur.fetchone():
                return None

            # Get freelancer profile id
            cur.execute("SELECT id FROM freelancer_profiles WHERE user_id = %s", (freelancer_id,))
            profile_row = cur.fetchone()
            if not profile_row:
                return None
            freelancer_profile_id = profile_row['id']

            cur.execute("""
                INSERT INTO job_applications (
                    job_id, freelancer_id, freelancer_profile_id, cover_letter,
                    proposed_rate, availability_date, status, applied_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                job_id,
                freelancer_id,
                freelancer_profile_id,
                application_data.get('cover_letter', ''),
                application_data.get('proposed_rate'),
                application_data.get('availability_date'),
                'applied',
                datetime.now(),
                datetime.now()
            ))
            app_id = cur.lastrowid

            # ✅ Update the job's applications_count
            cur.execute("UPDATE jobs SET applications_count = applications_count + 1 WHERE id = %s", (job_id,))

            conn.commit()
            return app_id
        except Exception as e:
            conn.rollback()
            print(f"Error creating job application: {e}")
            traceback.print_exc()
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(application_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT ja.*, 
                       j.title as job_title, 
                       j.recruiter_id,
                       u.first_name, 
                       u.last_name, 
                       u.email as freelancer_email,
                       fp.hourly_rate as freelancer_hourly_rate
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN users u ON ja.freelancer_id = u.id
                LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
                WHERE ja.id = %s
            """, (application_id,))
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_freelancer(freelancer_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT ja.*, j.title, j.pay_per_hour, j.experience_level, j.job_type,
                       u.first_name, u.last_name, rp.company_name
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN users u ON j.recruiter_id = u.id
                LEFT JOIN recruiter_profiles rp ON u.id = rp.user_id
                WHERE ja.freelancer_id = %s
                ORDER BY ja.applied_at DESC
            """, (freelancer_id,))
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_recent_by_freelancer(freelancer_id, limit=5):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT ja.*, j.title, j.pay_per_hour, j.experience_level,
                       rp.company_name
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                LEFT JOIN recruiter_profiles rp ON j.recruiter_id = rp.user_id
                WHERE ja.freelancer_id = %s
                ORDER BY ja.applied_at DESC
                LIMIT %s
            """, (freelancer_id, limit))
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_job(job_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT ja.*, u.first_name, u.last_name, u.email as freelancer_email,
                       fp.hourly_rate
                FROM job_applications ja
                JOIN users u ON ja.freelancer_id = u.id
                LEFT JOIN freelancer_profiles fp ON u.id = fp.user_id
                WHERE ja.job_id = %s
                ORDER BY ja.applied_at DESC
            """, (job_id,))
            rows = cur.fetchall()
            apps = []
            for row in rows:
                app = dict(row)
                # Fetch skills separately if needed
                cur2 = conn.cursor()
                cur2.execute("""
                    SELECT s.name
                    FROM freelancer_skills fs
                    JOIN skills s ON fs.skill_id = s.id
                    WHERE fs.freelancer_profile_id = (SELECT id FROM freelancer_profiles WHERE user_id = %s)
                """, (app['freelancer_id'],))
                app['skills'] = [r['name'] for r in cur2.fetchall()]
                cur2.close()
                apps.append(app)
            return apps
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_job_and_freelancer(job_id, freelancer_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id FROM job_applications
                WHERE job_id = %s AND freelancer_id = %s
            """, (job_id, freelancer_id))
            row = cur.fetchone()
            return row['id'] if row else None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_recent_for_recruiter(recruiter_id, limit=5):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT ja.*, j.title as job_title, u.first_name, u.last_name
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN users u ON ja.freelancer_id = u.id
                WHERE j.recruiter_id = %s
                ORDER BY ja.applied_at DESC
                LIMIT %s
            """, (recruiter_id, limit))
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_status(application_id, status, recruiter_notes=None):
        conn = get_connection()
        cur = conn.cursor()
        try:
            reviewed_at = None
            accepted_at = None
            rejected_at = None
            if status == 'reviewed':
                reviewed_at = datetime.now()
            elif status == 'accepted':
                accepted_at = datetime.now()
            elif status == 'rejected':
                rejected_at = datetime.now()

            cur.execute("""
                UPDATE job_applications
                SET status = %s, recruiter_notes = %s, updated_at = %s,
                    reviewed_at = COALESCE(%s, reviewed_at),
                    accepted_at = COALESCE(%s, accepted_at),
                    rejected_at = COALESCE(%s, rejected_at)
                WHERE id = %s
            """, (status, recruiter_notes, datetime.now(), reviewed_at, accepted_at, rejected_at, application_id))
            conn.commit()
            if cur.rowcount > 0:
                return JobApplication.get_by_id(application_id)
            return None
        except Exception as e:
            conn.rollback()
            print(f"Error updating application status: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def withdraw(application_id, freelancer_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                DELETE FROM job_applications
                WHERE id = %s AND freelancer_id = %s
            """, (application_id, freelancer_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error withdrawing application: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_job_ids(job_ids):
        if not job_ids:
            return []
        placeholders = ','.join(['%s'] * len(job_ids))
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(f"""
                SELECT ja.*, j.title as job_title,
                       CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
                       u.email as freelancer_email
                FROM job_applications ja
                JOIN jobs j ON ja.job_id = j.id
                JOIN users u ON ja.freelancer_id = u.id
                WHERE ja.job_id IN ({placeholders})
                ORDER BY ja.applied_at DESC
            """, job_ids)
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            conn.close()

# ==================== Notification Model ====================
class Notification:
    @staticmethod
    def create(user_id, title, message, notification_type,
               related_application_id=None, related_job_id=None):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO notifications (
                    user_id, title, message, notification_type,
                    related_application_id, related_job_id,
                    is_read, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, title, message, notification_type,
                related_application_id, related_job_id,
                False, datetime.now()
            ))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"Error creating notification: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_user(user_id, unread_only=False, limit=50):
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = """
                SELECT id, user_id, title, message, notification_type,
                       related_application_id, related_job_id, is_read, created_at
                FROM notifications
                WHERE user_id = %s
            """
            params = [user_id]
            if unread_only:
                query += " AND is_read = FALSE"
            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            rows = cur.fetchall()
            notifs = []
            for row in rows:
                notif = dict(row)
                notif['created_at'] = notif['created_at'].isoformat() if notif['created_at'] else None
                notifs.append(notif)
            return notifs
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_unread_count(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT COUNT(*) as count FROM notifications
                WHERE user_id = %s AND is_read = FALSE
            """, (user_id,))
            row = cur.fetchone()
            return row['count'] if row else 0
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def mark_as_read(notification_id, user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE notifications SET is_read = TRUE, read_at = %s
                WHERE id = %s AND user_id = %s
            """, (datetime.now(), notification_id, user_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error marking notification as read: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def mark_all_as_read(user_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE notifications SET is_read = TRUE, read_at = %s
                WHERE user_id = %s AND is_read = FALSE
            """, (datetime.now(), user_id))
            conn.commit()
            return cur.rowcount
        except Exception as e:
            conn.rollback()
            print(f"Error marking all notifications as read: {e}")
            return 0
        finally:
            cur.close()
            conn.close()