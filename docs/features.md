# Features

This document is intended to be a list of all features supported in SimDem

## Commands
* Execution - Command extracted from the document can be run in a separate shell
  * Shell - All command are run in a Linux shell. (PR for Powershell is welcome)
  * Comments - If command starts with `#`, it will be considered a comment and will not be run
* Validation - Validate if the previous command ran correctly.  See validation section for details
    * If validation passes - Continue processing
    * If validation fails - Exit program (default)
* Strip ANSI escape sequences

## Environment Variables
  * Allow the ability to inject environment variables via file or CLI (key/value format)

## Prerequisites
  * Allow ability to link to other SimDem documents to run.  (e.g. Need Azure CLI setup before creating resource group.)  Will be only run once
  * Validation - Validate if the prequisite requirements have been met.  See validation section for details
    * If validation passes - Don't run prerequisite document 
    * If validation fails - Continue to run prerequsite document

## Interrupt running
  * When running interactively, allow the ability to interrupt running document to run manual commands.  Resume processing document when complete

## Validation
  * Allows the output of the previous code block to be evaluated to determine if it meets an expected result.  Validation is either passed/failed.
  * Validation types
    * Expected Result Similarity - e.g. .80 match
    * Result Exact Match
    * Result Pattern Match
    * Exit code