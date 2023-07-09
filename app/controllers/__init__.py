def blueprints():
    from .main import bp as main_bp
    from .users_controllers import bp as users_bp
    from .movies_controllers import bp as movies_bp
    from .schools_controllers import bp as schools_bp
    from .linkages_controllers import bp as linkages_bp
    from .solicitations_controllers import bp as solicitations_bp
    

    return [main_bp, users_bp, movies_bp]
