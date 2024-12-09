Feature: Browse recipes
  As a user
  I want to browse a list of recipes
  So that I can find inspiration for my cooking

  Scenario: Viewing recipes
    Given there are recipes in the database
    When I visit the browse recipes page
    Then I should see a list of recipes