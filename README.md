## Overview

**NOTICE**: **SimDem is a proof of concept with lots of bugs. SimDem is undergoing a complete rewrite. As such, it is still in development and features may be removed or iterated on as we refine executable docs.**
**If you are able to contribute, we want your help!**

SimDem is an open source project that will provide tooling that empowers all people to write tutorials in markdown that then
becomes interactive documentation. Simdem works with standard markdown language and can be combined with any tutorial which run bash commands to create executable documentation which can be automatically tested for correctness through open source CI/CD tools and provides an interactive learning environment wherein individuals can truly learn best practices by **doing** rather than watching or reading

# Try it Out
## Run Executable Docs Using Azure Cloud Shell 
Azure Cloud Shell provides an environment with all of the prerequisites installed to run Simdem. This is the recommended method for new users to try and develop tutorials for simdem. 

Open [Azure Cloud Shell](https://ms.portal.azure.com/#cloudshell/) and select Bash as the environment. 

The following code snippet gets started with Simdem. 

>**Note** This snippet clones the Simdem repo, installs necessary dependencies, and runs the interactive Simdem tutorial script.

```
git clone https://github.com/Azure/simdem.git

cd simdem

pip3 install -r requirements.txt

python3 main.py tutorial simdem
```
The general format to run an executable document is: 
`python3 main.py <MODE_OF_OPERATION> <SCRIPT_DIRECTORY_NAME>`


## Run Executable Docs Using Local Machine
If you would like a more customizable development environment, or do not have an active Azure Subscription, Simdem can be run on a local machine with Python.

In Order to run and develop executable docs you need the following prerequisites.
* Python
* Pip3 (installed by default with python 3.4 or greater)
* A Linux Bash Shell

Run the following in a Linux Bash Shell on your local machine:

>**Note** This snippet clones the Simdem repo, installs necessary dependencies, and runs the interactive Simdem tutorial script.
```
git clone https://github.com/Azure/simdem.git

cd simdem

pip3 install -r requirements.txt

python3 main.py tutorial simdem
```

# Modes of Operation
You can run executable documents in four different modes:

  * Tutorial: Displays the descriptive text of the tutorial and pauses
    at code blocks to allow user interaction.
    `python3 main.py tutorial test`
  * Learn: Requires the user to type the complete command in order to move forward with execution. 
  `python3 main.py learn test`
  * Test: Runs the commands and then verifies that the output is
    sufficiently similar to the expected results (recorded in the
    markdown file) to be considered correct.
    `python3 main.py test test`
  * Demo: Runs the complete script continuously, only pausing when custom input is required.
  `python3 main.py demo test`
  * Script: Creates an executable bash script from the document
  `python3 main.py script test`

# Writing Your Own Executable Document

Writing your own executable document is easy to do. The first step to writing an executable document is to create a folder in the demo_scripts directory with the name of your document.

After creating the new folder, every simdem document needs two files.
  1. README.md 
  2. env.json 

The README.md is written in markdown and is the content which simdem parses and presents in an executable manner. For example [Azure Create VM readme.md](/demo_scripts/Azure/README.md)

The env.json file is a standard json file with default values for your executable document. This is critical for the automated testing aspect of simdem so that documents can be executed without any human interaction. For example
```json
{
    "MY_RESOURCE_GROUP_NAME": "myResourceGroup",
    "MY_LOCATION": "EastUS",
    "MY_VM_NAME": "myVM",
    "MY_USERNAME": "azureuser"
}
```

Once the README.md and env.json files have been successfully created, you can run your new document with the following command:

```bash
python3 main.py <MODE_OF_OPERATION> <SCRIPT_DIRECTORY_NAME>
```
## Example

The following is an example of how one might create their first executable document
```bash
cd demo_scripts
mkdir myCoolDocument
cd myCoolDocument
touch README.md
touch env.json
```
Once you add content to README.md and env.json the files, they can be run in an executable manner with the following command:

```bash
python3 main.py tutorial myCoolDocument
```

## Learn More About Writing Your Own Executable Document
To learn more about writing executable documentation use the interactive tutorial by running:
 ```
 python3 main.py tutorial simdem
 ```


# Setting up CI/CD with Github Actions
**In Progress**


# Contributing

This is an open source project. Don't keep your code improvements,
features and cool ideas to yourself. Please issue pull requests
against our [GitHub repo](http://github.com/rgardler/simdem).

Be sure to use our Git pre-commit script to test your contributions
before committing, simply run the following command:

```
ln -s ../../pre-commit.sh .git/hooks/pre-commit
```

This project welcomes contributions and suggestions.  Most
contributions require you to agree to a Contributor License Agreement
(CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine
whether you need to provide a CLA and decorate the PR appropriately
(e.g., label, comment). Simply follow the instructions provided by the
bot. You will only need to do this once across all repos using our
CLA.

This project has adopted
the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see
the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with
any additional questions or comments.

## Publishing

The `latest` version is built from source on each commit. To publish a
version tagged image use `./scripts/publish.sh <FLAVOR>` script. This
will publish both the CLI and NoVNC containers if no `FLAVOR` is
provided.

Don't forget to bump the version number after using this script. To do
this open simdem.py and find and edit the following line (somewhere
near the top of the file):

`SIMDEM_VERSION = "0.4.1"`

# Learn more

If you want to learn more before running the program then why not
read the interactive tutorial as
a
[markdown page on GitHub](https://github.com/Azure/simdem/tree/main/demo_scripts/simdem).
