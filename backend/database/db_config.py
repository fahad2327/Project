import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'freelancer_portal'),
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4',
            autocommit=False
        )
        return connection
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e

def init_database():
    """Initialize database and create all tables"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Create Skills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Tech Stacks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tech_stacks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            email VARCHAR(254) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            user_type ENUM('freelancer', 'recruiter') NOT NULL,
            profile_picture VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            is_verified BOOLEAN DEFAULT FALSE,
            last_login TIMESTAMP NULL,
            date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_username (username),
            INDEX idx_user_type (user_type)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Freelancer Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS freelancer_profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            bio TEXT,
            hourly_rate DECIMAL(10, 2),
            education TEXT,
            experience TEXT,
            years_of_experience INT DEFAULT 0,
            profile_picture VARCHAR(255),
            resume_url VARCHAR(255),
            github_url VARCHAR(255),
            linkedin_url VARCHAR(255),
            portfolio_url VARCHAR(255),
            is_available BOOLEAN DEFAULT TRUE,
            total_projects INT DEFAULT 0,
            success_rate DECIMAL(5, 2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_hourly_rate (hourly_rate),
            INDEX idx_is_available (is_available)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Freelancer Skills (Many-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS freelancer_skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            freelancer_profile_id INT NOT NULL,
            skill_id INT NOT NULL,
            proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (freelancer_profile_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
            UNIQUE KEY unique_freelancer_skill (freelancer_profile_id, skill_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Freelancer Tech Stacks (Many-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS freelancer_tech_stacks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            freelancer_profile_id INT NOT NULL,
            tech_stack_id INT NOT NULL,
            experience_years INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (freelancer_profile_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (tech_stack_id) REFERENCES tech_stacks(id) ON DELETE CASCADE,
            UNIQUE KEY unique_freelancer_tech (freelancer_profile_id, tech_stack_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Recruiter Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recruiter_profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            company_name VARCHAR(200) NOT NULL,
            company_website VARCHAR(255),
            company_size VARCHAR(50),
            industry VARCHAR(100),
            company_description TEXT,
            company_logo VARCHAR(255),
            location VARCHAR(200),
            phone VARCHAR(20),
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_company_name (company_name),
            INDEX idx_is_verified (is_verified)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            recruiter_id INT NOT NULL,
            recruiter_profile_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            pay_per_hour DECIMAL(10, 2) NOT NULL,
            experience_level ENUM('junior', 'mid', 'senior') NOT NULL,
            job_type ENUM('full-time', 'part-time', 'contract', 'freelance') DEFAULT 'freelance',
            location VARCHAR(200),
            is_remote BOOLEAN DEFAULT TRUE,
            requirements TEXT,
            responsibilities TEXT,
            benefits TEXT,
            application_deadline DATE,
            is_active BOOLEAN DEFAULT TRUE,
            views_count INT DEFAULT 0,
            applications_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_profile_id) REFERENCES recruiter_profiles(id) ON DELETE CASCADE,
            INDEX idx_title (title),
            INDEX idx_experience_level (experience_level),
            INDEX idx_is_active (is_active),
            INDEX idx_created_at (created_at),
            INDEX idx_pay_per_hour (pay_per_hour),
            FULLTEXT INDEX idx_job_search (title, description, requirements)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Job Skills (Many-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT NOT NULL,
            skill_id INT NOT NULL,
            is_required BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
            UNIQUE KEY unique_job_skill (job_id, skill_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Job Tech Stacks (Many-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_tech_stacks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT NOT NULL,
            tech_stack_id INT NOT NULL,
            is_required BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY (tech_stack_id) REFERENCES tech_stacks(id) ON DELETE CASCADE,
            UNIQUE KEY unique_job_tech (job_id, tech_stack_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Job Applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT NOT NULL,
            freelancer_id INT NOT NULL,
            freelancer_profile_id INT NOT NULL,
            cover_letter TEXT,
            proposed_rate DECIMAL(10, 2),
            availability_date DATE,
            status ENUM('applied', 'reviewed', 'shortlisted', 'accepted', 'rejected') DEFAULT 'applied',
            recruiter_notes TEXT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewed_at TIMESTAMP NULL,
            accepted_at TIMESTAMP NULL,
            rejected_at TIMESTAMP NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY (freelancer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (freelancer_profile_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE,
            UNIQUE KEY unique_application (job_id, freelancer_id),
            INDEX idx_status (status),
            INDEX idx_applied_at (applied_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Create Notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            notification_type ENUM('application', 'job', 'profile', 'system') DEFAULT 'application',
            related_application_id INT,
            related_job_id INT,
            is_read BOOLEAN DEFAULT FALSE,
            is_email_sent BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (related_application_id) REFERENCES job_applications(id) ON DELETE SET NULL,
            FOREIGN KEY (related_job_id) REFERENCES jobs(id) ON DELETE SET NULL,
            INDEX idx_user_id (user_id),
            INDEX idx_is_read (is_read),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Database initialized successfully!")