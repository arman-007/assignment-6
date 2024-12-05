# Property Management System

## Overview

The Property Management System is a Django-based application designed to manage property information efficiently. It leverages Django's powerful Admin interface to create, update, and manage properties, while using PostgreSQL with PostGIS extensions to handle geospatial data for property locations. The project aims to provide a robust platform for property owners to list and manage properties, complete with sign-up and approval workflows for new users.

Key Features:
- Property owners can sign up, manage, and list their properties.
- Admin panel allows superusers to approve new users.
- Integration of PostGIS for geospatial data management.
- Role-based access control, with property owners only able to manage their own listings.

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/arman-007/assignment-6.git
   cd assignment-6
   ```

2. **Set Up the Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
   This instruction is for linux/mac.

## Docker Instructions

To run the project using Docker, follow these steps:

1. **Build and Run Docker Containers**
   Ensure you have Docker and Docker Compose installed. Then, use the following commands to build and run the containers:
   ```bash
   docker compose build
   ```
   ```bash
   docker compose up
   ```

   This will start both the PostgreSQL/PostGIS container and the Django application container.


2. **Apply Migrations in Docker**
   After the containers are up, run the migrations inside the Django container:
   ```bash
   docker exec -it assignment-6-web-1 python manage.py migrate
   ```

3. **Create a Superuser in Docker**
   Create a superuser to access the admin panel:
   ```bash
   docker exec -it assignment-6-web-1 python manage.py createsuperuser
   ```

4. **Access the Application**
   - The Django application will be available at `http://127.0.0.1:8000`.
   - The admin panel can be accessed at `http://127.0.0.1:8000/admin`.

## How to Use

### Admin Panel
- Access the Django admin panel at `http://127.0.0.1:8000/admin`.
- Use your superuser credentials to log in.
- From here, you can manage properties, users, and other data.
- Approve newly registered users by marking them as staff and assigning them the "Property Owner" group.

### Property Owner Portal
- Property owners can sign up through the public-facing sign-up page (`/accounts/signup/`).
- Once approved, they will be able to log in, view their properties, and manage them through the admin panel.

### Adding Properties
- After logging in, property owners can add new properties.
- Geolocation (latitude and longitude) is required for each property and should be added as a PointField.
- Images can be added via URLs, which are stored in an array.

### Sitemap Generation
- Use the command-line utility to generate a sitemap for properties.
- Run the command:
  ```bash
  python manage.py generate_sitemap
  ```
  This will create a `sitemap.json` containing all property locations.

## Special Optimizations and Features
- **Django Allauth for Authentication**: The project uses Django Allauth to handle user authentication, providing a seamless sign-up, login, and account management experience.
- **PostGIS Integration**: Utilizes PostGIS to store and manage geospatial data, making it easier to handle properties' geographic locations.
- **Partitioning**: Database tables for properties are partitioned based on specific columns for efficient querying.
- **Admin User Workflow**: New users require admin approval before they can manage properties, ensuring security and data integrity.
- **Role-Based Access Control**: The application provides different access levels, ensuring that property owners can only access and manage their own properties.
- **Custom Command for Sitemap Generation**: The project includes a custom Django command to generate a JSON sitemap for all property locations, facilitating SEO and property discovery.

## Future Improvements
- **Front-end Interface**: Expand to include a dedicated front-end with React or Vue for enhanced user experience.
- **Integration with External APIs**: Integrate with Google Maps for geocoding and location-based services.
- **Advanced Analytics**: Add analytics for property views and inquiries, providing insights for property owners.

Feel free to contribute to this project by creating issues or submitting pull requests. We welcome all feedback and suggestions to improve the project.

