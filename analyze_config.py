import os
import json

class Neo4jConfigAnalyzer:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read_config(self):
        config = {}
        with open(self.config_file_path, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    key, value = map(str.strip, line.split('=', 1))
                    config[key] = value
        return config

    def check_security_settings(self, config):
        results = []

        # Check authentication and authorization settings
        auth_enabled = config.get("dbms.security.auth_enabled", "true").lower() == "true"
        results.append({
            "setting": "dbms.security.auth_enabled",
            "value": config.get("dbms.security.auth_enabled"),
            "status": "OK" if auth_enabled else "NOT OK",
            "recommendation": "Ensure authentication is enabled (dbms.security.auth_enabled=true)" if not auth_enabled else "Authentication is enabled"
        })

        unrestricted_procedures = "dbms.security.procedures.unrestricted" in config
        results.append({
            "setting": "dbms.security.procedures.unrestricted",
            "value": config.get("dbms.security.procedures.unrestricted"),
            "status": "NOT OK" if unrestricted_procedures else "OK",
            "recommendation": "Avoid unrestricted procedures (dbms.security.procedures.unrestricted)" if unrestricted_procedures else "No unrestricted procedures found"
        })

        auth_listen_address = config.get("dbms.security.auth_listen_address")
        if auth_listen_address:
            open_auth_listen = auth_listen_address == "0.0.0.0" or auth_listen_address.startswith("0.0.0.")
            results.append({
                "setting": "dbms.security.auth_listen_address",
                "value": auth_listen_address,
                "status": "NOT OK" if open_auth_listen else "OK",
                "recommendation": "Restrict the authentication server to specific IP addresses (dbms.security.auth_listen_address)" if open_auth_listen else "Authentication listen address is restricted"
            })

        # Check network settings
        bolt_address = config.get("dbms.connector.bolt.listen_address")
        if bolt_address:
            open_bolt_address = bolt_address == "0.0.0.0" or bolt_address.startswith("0.0.0.")
            results.append({
                "setting": "dbms.connector.bolt.listen_address",
                "value": bolt_address,
                "status": "NOT OK" if open_bolt_address else "OK",
                "recommendation": "Restrict the Bolt connector to specific IP addresses (dbms.connector.bolt.listen_address)" if open_bolt_address else "Bolt listen address is restricted"
            })

        http_address = config.get("dbms.connector.http.listen_address")
        if http_address:
            open_http_address = http_address == "0.0.0.0" or http_address.startswith("0.0.0.")
            results.append({
                "setting": "dbms.connector.http.listen_address",
                "value": http_address,
                "status": "NOT OK" if open_http_address else "OK",
                "recommendation": "Restrict the HTTP connector to specific IP addresses (dbms.connector.http.listen_address)" if open_http_address else "HTTP listen address is restricted"
            })

        https_address = config.get("dbms.connector.https.listen_address")
        if https_address:
            open_https_address = https_address == "0.0.0.0" or https_address.startswith("0.0.0.")
            results.append({
                "setting": "dbms.connector.https.listen_address",
                "value": https_address,
                "status": "NOT OK" if open_https_address else "OK",
                "recommendation": "Restrict the HTTPS connector to specific IP addresses (dbms.connector.https.listen_address)" if open_https_address else "HTTPS listen address is restricted"
            })

        # Check logging and monitoring settings
        query_logging_enabled = config.get("dbms.logs.query.enabled", "false").lower() == "true"
        results.append({
            "setting": "dbms.logs.query.enabled",
            "value": config.get("dbms.logs.query.enabled"),
            "status": "OK" if query_logging_enabled else "NOT OK",
            "recommendation": "Enable query logging for auditing (dbms.logs.query.enabled=true)" if not query_logging_enabled else "Query logging is enabled"
        })

        debug_level = config.get("dbms.logs.debug.level")
        if debug_level:
            debug_level_safe = debug_level.lower() != "debug"
            results.append({
                "setting": "dbms.logs.debug.level",
                "value": debug_level,
                "status": "NOT OK" if not debug_level_safe else "OK",
                "recommendation": "Set debug logging level to a non-sensitive level (dbms.logs.debug.level)" if not debug_level_safe else "Debug logging level is set appropriately"
            })

        # Check data security settings
        import_directory = config.get("dbms.directories.import")
        if import_directory:
            import_directory_safe = import_directory != "/tmp" and import_directory != "/var/tmp"
            results.append({
                "setting": "dbms.directories.import",
                "value": import_directory,
                "status": "NOT OK" if not import_directory_safe else "OK",
                "recommendation": "Set import directory to a secure location (dbms.directories.import)" if not import_directory_safe else "Import directory is set to a secure location"
            })

        csv_import_allowed = config.get("dbms.security.allow_csv_import_from_file_urls", "false").lower() == "true"
        results.append({
            "setting": "dbms.security.allow_csv_import_from_file_urls",
            "value": config.get("dbms.security.allow_csv_import_from_file_urls"),
            "status": "NOT OK" if csv_import_allowed else "OK",
            "recommendation": "Disallow CSV import from file URLs for security (dbms.security.allow_csv_import_from_file_urls=false)" if csv_import_allowed else "CSV import from file URLs is disallowed"
        })

        # Check SSL settings
        ssl_policy_enabled = config.get("dbms.ssl.policy.default.enabled", "false").lower() == "true"
        results.append({
            "setting": "dbms.ssl.policy.default.enabled",
            "value": config.get("dbms.ssl.policy.default.enabled"),
            "status": "OK" if ssl_policy_enabled else "NOT OK",
            "recommendation": "Enable SSL policy for secure communication (dbms.ssl.policy.default.enabled=true)" if not ssl_policy_enabled else "SSL policy is enabled"
        })

        # Check backups
        backup_enabled = config.get("dbms.backup.enabled", "false").lower() == "true"
        results.append({
            "setting": "dbms.backup.enabled",
            "value": config.get("dbms.backup.enabled"),
            "status": "OK" if backup_enabled else "NOT OK",
            "recommendation": "Enable backups for data safety (dbms.backup.enabled=true)" if not backup_enabled else "Backups are enabled"
        })

        # Check transaction logs
        tx_log_rotation_size = config.get("dbms.tx_log.rotation.size")
        if tx_log_rotation_size:
            tx_log_rotation_size_safe = int(tx_log_rotation_size.strip('M')) > 10
            results.append({
                "setting": "dbms.tx_log.rotation.size",
                "value": tx_log_rotation_size,
                "status": "OK" if tx_log_rotation_size_safe else "NOT OK",
                "recommendation": "Set transaction log rotation size to at least 10M (dbms.tx_log.rotation.size)" if not tx_log_rotation_size_safe else "Transaction log rotation size is adequate"
            })

        return results

    def analyze_config(self):
        config = self.read_config()
        results = self.check_security_settings(config)
        return results

# Example usage
config_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/conf/neo4j.conf"

analyzer = Neo4jConfigAnalyzer(config_file_path)
security_issues = analyzer.analyze_config()

