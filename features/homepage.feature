# Created by whwong at 20/4/17
Feature: Home Page

  Scenario: Visit homepage
    Given a user visits the site
    Then she should see Flaskr

  Scenario: Login Link
    Given a user visits the site
    And she is not logged in
    Then she should see the Login link

  Scenario: Logout Link
    Given a user visits the site
    When she logs in
    And she returns to the site
    Then she should see the Logout link
