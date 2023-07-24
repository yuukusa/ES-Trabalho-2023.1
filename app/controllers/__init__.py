def blueprints():
    from .main import bp as main_bp
    from .users_controllers import bp as users_bp
    from .questions_controllers import bp as questions_bp
    from .exams_controllers import bp as exams_bp
    from .exams_mounted_controllers import bp as exams_mounted_bp
    
    

    return [main_bp, users_bp, questions_bp, exams_bp, exams_mounted_bp]
