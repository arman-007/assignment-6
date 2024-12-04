from django.db import migrations, models

def create_partitioned_table(apps, schema_editor):
    # Drop the existing table
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS inventory_accommodation CASCADE;
        """)

        # Create the partitioned table with 'feed' as part of the partition key
        cursor.execute("""
            CREATE TABLE inventory_accommodation (
                id SERIAL,
                feed SMALLINT NOT NULL,
                title VARCHAR(100),
                country_code CHAR(2),
                bedroom_count INTEGER,
                review_score DECIMAL(2, 1) DEFAULT 0,
                usd_rate DECIMAL(10, 2),
                center GEOMETRY(Point, 4326),
                images TEXT[],
                location_id INTEGER,
                amenities TEXT[],
                user_id INTEGER,
                published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT pk_accommodation PRIMARY KEY (id, feed),
                CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES inventory_location(id) ON DELETE CASCADE
            ) PARTITION BY RANGE (feed);
        """)

        # Create partitions for each feed range
        for i in range(8):
            lower = i * 4096
            upper = (i + 1) * 4095
            cursor.execute(f"""
                CREATE TABLE inventory_accommodation_feed_{i + 1} PARTITION OF inventory_accommodation
                FOR VALUES FROM ({lower}) TO ({upper});
            """)

def reverse_partitioning(apps, schema_editor):
    # Drop the partitioned table and recreate it without partitioning
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS inventory_accommodation CASCADE;
        """)

        # Create the non-partitioned table
        cursor.execute("""
            CREATE TABLE inventory_accommodation (
                id SERIAL PRIMARY KEY,
                feed SMALLINT NOT NULL,
                title VARCHAR(100) NOT NULL,
                country_code CHAR(2) NOT NULL,
                bedroom_count INTEGER NOT NULL,
                review_score DECIMAL(2,1) NOT NULL DEFAULT 0,
                usd_rate DECIMAL(10,2) NOT NULL,
                center GEOMETRY,
                images TEXT[],
                location_id INTEGER NOT NULL,
                amenities TEXT[],
                user_id INTEGER,
                published BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES inventory_location(id) ON DELETE CASCADE,
                CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES auth_user(id)
            );
        """)

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_accommodation_location_id_and_more'),  # Adjust to your last migration
    ]

    operations = [
        migrations.RunPython(create_partitioned_table, reverse_partitioning),
    ]
