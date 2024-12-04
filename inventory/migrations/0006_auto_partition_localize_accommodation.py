from django.db import migrations, models

def create_partitioned_table(apps, schema_editor):
    # Drop the existing table
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS inventory_localizeaccommodation CASCADE;
        """)

        # Create the partitioned table
        cursor.execute("""
            CREATE TABLE inventory_localizeaccommodation (
                id SERIAL,
                property_id INTEGER NOT NULL,
                language CHAR(2) NOT NULL,
                description TEXT,
                policy JSONB DEFAULT '{}'::jsonb,
                CONSTRAINT fk_property FOREIGN KEY(property_id) REFERENCES inventory_accommodation(id) ON DELETE CASCADE,
                PRIMARY KEY (id, language)  -- Include 'language' in the primary key
            ) PARTITION BY LIST (language);
        """)

        # Create partitions for each language in the LanguageCode enum
        for lang in ['en', 'fr', 'es', 'de', 'it', 'pt', 'zh', 'ar', 'ja', 'ru', 'bn', 'hi', 'ur', 'ko', 'tr', 'pl', 'nl', 'sv', 'el', 'ro', 'da', 'fi', 'cs', 'hu']:
            cursor.execute(f"""
                CREATE TABLE inventory_localizeaccommodation_{lang} PARTITION OF inventory_localizeaccommodation
                FOR VALUES IN ('{lang}');
            """)

def reverse_partitioning(apps, schema_editor):
    # Drop the partitioned table and recreate it without partitioning
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS inventory_localizeaccommodation CASCADE;
        """)

        # Create the non-partitioned table
        cursor.execute("""
            CREATE TABLE inventory_localizeaccommodation (
                id SERIAL PRIMARY KEY,
                property_id INTEGER,
                language CHAR(2),
                description TEXT,
                policy JSONB
            );
        """)

class Migration(migrations.Migration):

    dependencies = [
        # Add the dependency for the migration where the LocalizeAccommodation model was defined
        ('inventory', '0005_alter_location_location_type'),
    ]

    operations = [
        migrations.RunPython(create_partitioned_table, reverse_partitioning),
    ]
