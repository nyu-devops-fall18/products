Feature: The product store service back-end
	As a Product Store Owner
	I need a RESTful catalog service
	So that I can keep track of all my products

Background:
	Given the following products
		| id | name         |     description   |  category  | price | condition | inventory | review   | rating |
		|  1 | Athens Table |    Stupid Table   |   Table    |  20   |   Boxed   |     2     | Great!   |   10   |
		|  2 | Rome Chair   |    Stupid Chair   |   Chair    |  40   |   Boxed   |     5     | Okay!    |   8    |

Scenario: The server is running
	When I visit the "Home Page"
	Then I should see "Product Demo RESTful Service" in the title
	And I should not see "404 Not Found"

Scenario: Create a Product
	When I visit the "Home Page"
	And I set the "Name" to "Greek Bath Tub"
	And I set the "Category" to "Bath"
	And I set the "Description" to "Stupid Tub"
	And I set the "Price" to "40"
	And I set the "Condition" to "Open"
	And I set the "Inventory" to "10"
	And I set the "Review" to "So So"
	And I set the "Rating" to "8"
	And I press the "Create" button
	Then I should see the message "Success"

Scenario: List all products
	When I visit the "Home Page"
	And I press the "Search" button
	Then I should see "Athens Table" in the results
	And I should see "Rome Chair" in the results

Scenario: List all tables
	When I visit the "Home Page"
	And I set the "Category" to "Table"
	And I press the "Search" button
	Then I should see "Athens Table" in the results
	And I should not see "Rome Chair" in the results

Scenario: Update a Product
	When I visit the "Home Page"
	And I set the "Id" to "1"
	And I press the "Retrieve" button
	Then I should see "Athens Table" in the "Name" field
	When I change "Name" to "Italian Table"
	And I press the "Update" button
	Then I should see the message "Success"
	When I set the "Id" to "1"
	And I press the "Retrieve" button
	Then I should see "Italian Table" in the "Name" field
	When I press the "Clear" button
	And I press the "Search" button
	Then I should see "Italian Table" in the results
	Then I should not see "Athens Table" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Id" to "2"
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should not see "Rome Chair" in the results

Scenario: Add a Rating to a product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I set the "Rating" to "8"
    And I press the "Rating" button
    Then I should see the message "Success"       
    When I press the "Clear" button
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "9" in the "Rating" field
