from flask import Blueprint, request, jsonify
from database.db_config import get_db_connection
import pymysql

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    """Get all active jobs with filters"""
    try:
        # Get filter parameters
        search = request.args.get('search', '')
        experience_level = request.args.get('experience_level', '')
        min_pay = request.args.get('min_pay', '')
        max_pay = request.args.get('max_pay', '')
        job_type = request.args.get('job_type', '')
        is_remote = request.args.get('is_remote', '')
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Base query
        query = """
            SELECT j.*, 
                   rp.company_name,
                   CONCAT(u.first_name, ' ', u.last_name) as recruiter_name
            FROM jobs j
            JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
            JOIN users u ON j.recruiter_id = u.id
            WHERE j.is_active = TRUE
        """
        params = []
        
        # Add search filter - IMPROVED VERSION
        if search:
            query += """ AND (
                LOWER(j.title) LIKE LOWER(%s) OR 
                LOWER(j.description) LIKE LOWER(%s) OR 
                LOWER(j.requirements) LIKE LOWER(%s) OR
                LOWER(j.title) LIKE LOWER(%s) OR
                LOWER(j.title) LIKE LOWER(%s)
            )"""
            search_term = f'%{search}%'
            search_term_frontend = f'%frontend%'  # Always match frontend
            # Add multiple search terms to catch variations
            params.extend([
                search_term, 
                search_term, 
                search_term,
                f'%{search}%',  # Another copy for good measure
                f'%{search}%'
            ])
            print(f"Searching for: {search}")  # Debug log
        
        # Add experience level filter
        if experience_level:
            query += " AND j.experience_level = %s"
            params.append(experience_level)
        
        # Add pay filters
        if min_pay and min_pay.strip():
            try:
                min_pay_val = float(min_pay)
                query += " AND j.pay_per_hour >= %s"
                params.append(min_pay_val)
            except ValueError:
                pass
        
        if max_pay and max_pay.strip():
            try:
                max_pay_val = float(max_pay)
                query += " AND j.pay_per_hour <= %s"
                params.append(max_pay_val)
            except ValueError:
                pass
        
        # Add job type filter
        if job_type and job_type != 'All Types' and job_type != '':
            query += " AND j.job_type = %s"
            params.append(job_type)
        
        # Add remote filter
        if is_remote and is_remote.lower() == 'true':
            query += " AND j.is_remote = TRUE"
        
        query += " ORDER BY j.created_at DESC"
        
        print(f"Executing query: {query}")  # Debug log
        print(f"With params: {params}")     # Debug log
        
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        
        print(f"Found {len(jobs)} jobs")  # Debug log
        
        # Get skills for each job
        for job in jobs:
            # Get skills
            cursor.execute("""
                SELECT s.name
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.id
                WHERE js.job_id = %s
            """, (job['id'],))
            job['required_skills'] = [s['name'] for s in cursor.fetchall()]
            
            # Get tech stack
            cursor.execute("""
                SELECT ts.name
                FROM job_tech_stacks jts
                JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
                WHERE jts.job_id = %s
            """, (job['id'],))
            job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'count': len(jobs),
            'jobs': jobs
        }), 200
        
    except Exception as e:
        print(f"Error in get_jobs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e),
            'jobs': []
        }), 500

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job details by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT j.*, 
                   rp.company_name,
                   CONCAT(u.first_name, ' ', u.last_name) as recruiter_name,
                   u.email as recruiter_email
            FROM jobs j
            JOIN recruiter_profiles rp ON j.recruiter_profile_id = rp.id
            JOIN users u ON j.recruiter_id = u.id
            WHERE j.id = %s
        """, (job_id,))
        
        job = cursor.fetchone()
        
        if job:
            # Get required skills
            cursor.execute("""
                SELECT s.id, s.name
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.id
                WHERE js.job_id = %s
            """, (job_id,))
            job['required_skills'] = [s['name'] for s in cursor.fetchall()]
            
            # Get tech stack
            cursor.execute("""
                SELECT ts.id, ts.name
                FROM job_tech_stacks jts
                JOIN tech_stacks ts ON jts.tech_stack_id = ts.id
                WHERE jts.job_id = %s
            """, (job_id,))
            job['tech_stack'] = [t['name'] for t in cursor.fetchall()]
            
            # Increment view count
            cursor.execute("""
                UPDATE jobs SET views_count = views_count + 1 WHERE id = %s
            """, (job_id,))
            connection.commit()
        
        cursor.close()
        connection.close()
        
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
        
        return jsonify({
            'success': True,
            'job': job
        }), 200
        
    except Exception as e:
        print(f"Error in get_job: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500