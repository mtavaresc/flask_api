Feature: Operations related to Users

  Scenario: Creating a new user
    Given the API service is running
    When i send a post request with "admin" and "admin_password"
    Then i should see the data user response