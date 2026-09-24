---
title: "01. User administration & set up"
weight: 7
---
In this module, we will configure settings for a pre-provisioned AWS IAM Identity Center (IDC) user named **dg-corp-admin**. This user will access **Amazon SageMaker Unified Studio** in later modules to work with financial services data spanning core banking, trading, and risk management systems. You'll learn how to set up user access for a unified data platform that enables CFO-level analytics across market data, trade executions, and risk metrics.

### Set New User Password

1. Navigate to the [IAM Identity Center Console](https://us-east-1.console.aws.amazon.com/singlesignon/home?region=us-east-1), select **Users** from the left navigation menu.

2. Select **dg-corp-admin** and from the user page, choose the **Reset password** button in the top right corner

![Reset Password](/static/images/02studio/resetpwd.jpeg)

3. In the reset password pop-up, select the second option, *Generate a one-time password and share the password with the user* and choose **Reset password**

![Generate Password](/static/images/02studio/generatepwd.jpeg)

4. Make a note of the following credentials: AWS access portal URL and One-time password

![Save Credentials](/static/images/02studio/savepwd.jpeg)

5. Open the **AWS access portal URL** in a new tab, when prompted enter the username, :code[dg-corp-admin]{showCopyAction=true} and the temporary password from the previous step

6. When prompted, create your new password, for example :code[SageMaker@N3XTGEN]{showCopyAction=true}. This will take you into your AWS access portal.

![Set New Password](/static/images/02studio/setpwd.jpeg)

### Access your Amazon SageMaker environment

1. From within your portal, locate and select the **Amazon SageMaker** application tile. Choose **Sign in with SSO** when prompted

![Access portal](/static/images/sso.png)

2. As part of the account setup, we have configured one domain for you called **Corporate** with one project that we will be working within. Locate the "Select a project" dropdown at the top of the page. Choose the pre-created project: **AnyCompany SM Unified Data AI** to be taken to the project overview page.

![Access portal](/static/images/proj.png)


::alert[You've successfully accessed your SageMaker Unified Studio project. Please leave this tab open as we will come back to this portal in future modules.]{header="Success!" type="success"}