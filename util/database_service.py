import yaml
import mysql.connector


class DatabaseService:
    def __init__(self, config_path='config/config.yml'):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        db_config = config['database']

        self.connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        self.cursor = self.connection.cursor()

    def add_user_info(self, user_info):
        sql = """
        INSERT INTO user_info(question, address, header, create_time, uuid, answer, model, msg)
        VALUES (%s, %s ,%s ,%s, %s, %s, %s, %s)
        """
        values = (
            user_info['question'],
            user_info['address'],
            user_info['header'],
            user_info['create_time'],
            user_info['uuid'],
            user_info['answer'],
            user_info['model'],
            user_info['msg']
        )
        self.cursor.execute(sql, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def add_ip_info(self, ip_info, location):
        sql = """
        INSERT INTO ip_info(country, countryCode, regionName, city, lat, lon, isp, org, as1, query, uuid, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            ip_info['country'],
            ip_info['countryCode'],
            ip_info['regionName'],
            ip_info['city'],
            ip_info['lat'],
            ip_info['lon'],
            ip_info['isp'],
            ip_info['org'],
            ip_info['as'],
            ip_info['query'],
            ip_info['uuid'],
            location
        )
        self.cursor.execute(sql, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user_info(self):
        self.cursor.execute("""
            SELECT 
            u.question, 
            u.answer, 
            u.model,
            u.msg,
            u.address, 
            i.location, 
            i.country, 
            i.countryCode, 
            i.regionName, 
            i.city, 
            i.lat, 
            i.lon, 
            i.isp, 
            i.org, 
            i.as1, 
            u.create_time  
            FROM 
            user_info u 
            LEFT JOIN ip_info i ON ( u.uuid = i.uuid )  
            ORDER BY 
            u.id DESC
        """)
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.connection.close()
