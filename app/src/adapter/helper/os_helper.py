import os


class OsHelper:
    @staticmethod
    def get_required_env(env_name):
        env_value = os.getenv(env_name)

        if env_value is None:
            raise Exception("env '", env_name, "' not found.")

        return env_value
