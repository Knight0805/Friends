# Django Rate-Limited Friend Requests

This Django project demonstrates how to implement rate limiting and friend request functionality using Django and DRF.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.x
- Django
- Django REST framework
- (Other dependencies)

### Installation

1. Clone the repository:

   ```
   git clone git@github.com:A1man1/Django_Login-Friends_view.git

   ```
   Navigate to the project directory:

cd django-rate-limited-friend-requests

Install dependencies:

bash

pip install -r requirements.txt

Apply database migrations:

bash

    python manage.py migrate

Usage

    Run the development server:

    bash

    python manage.py runserver

    Access the API at http://localhost:8000/.

Rate Limiting

    Rate limiting is implemented using a custom decorator (custom_ratelimiter) that checks the number of requests made within a specified time frame.

Friend Requests

    Friend requests are implemented using Django models (FriendRequest) and Django REST framework serializers.
    Users can send friend requests to each other, and the requests are recorded in the database.
    Rate limiting is applied to the friend request endpoint to prevent abuse.

Contributing

If you'd like to contribute to this project, please follow these steps:

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Make your changes and commit them.
    Push to your fork and submit a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Mention any libraries or frameworks you used.
    Give credit to other developers or resources that inspired your project.

vbnet


Replace placeholders like `A1man1` with your actual GitHub username and