# CAT-tax
Capital-gain Automated Transactions (CAT)

Self-assessment tax returns for capital gains is deceptively difficult to report because there are multiple types of shares: Same day shares, bed and breakfast rule and Section 104 (https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg51560). The shares depends on how much time has elapsed between a share being bought and sold, and that changes the profit and loss calculations. It also depends on previous and subsequent transactions in other tax years.

Since there are no tools online to do so, this is a tool to simplify the process. This is an interface to upload required files and outputs a compliant tax return form.

The ambition of the tool is to simulate it on localstack, to test how the tool would work if it was industralised on cloud (i.e. if there are many different users, they can upload new stock transactions and obtain a HMRC-ready output).

It is separated into the following stages and their branch:
1. Generate random inputs to test the code - feat/gen-inputs
2. Develop inputs management (excel to start with) - feat/simple-inputs
3. Calculates the capital gains following HMRC's rules (including same day, bed and breakfast rules and Section 104) https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg51560
4. Outputs the results into a HMRC valid output
5. Create a user interface to deal with inputs
6. Simulate AWS services on localstack for a full CAT tax service, where user can go back to the same service every year with data saved.


