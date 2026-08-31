# CI trigger

This file intentionally exists to trigger the real Hudi integration workflow on push.

The workflow must compile the custom Hudi merger and execute the Spark/Hudi validation before distributed runtime claims are made.
