Sample code projects for building security applications using Symantec Cloud Workload Protection REST API

Before you get started you need a Symantec Cloud Workload Protection Account. If you do not have one sign up for a trial account using this link, select the 'Cloud Workload Protection' check box: https://securitycloud.symantec.com/cc/#/onboard?CID=70138000001QHo5AAG&pr_id=F979E61C-A412-4A58-8879-B83E25B7327F#/onboard

You can also buy Cloud Workload protection from Amazon AWS Market Place that also includes free usage. Click this link: https://aws.amazon.com/marketplace/pp/B0722D4QRN

After you have activated your account, completed AWS, Azure or Google Cloud Connection; deployed CWP agent on our cloud instances, you are ready to start using these samples

First step is to Create API access keys. After login to CWP console, go to 'Settings' page and click on 'API Keys' tab

Copy following API secret keys and your CWP tenant ID information and keep themsafe

Customer ID: SEJ*#########################7788

Domain ID: Dq*####################6Yh

Client ID: O***#####################y988

Client Secret Key: t##################################

Code Files

cwpagentinstall.py This python script downloads CWP agent installer from your CWP account, saves the files locally, runs the agent installer and reboots the instance. You can insert this script in your AWS instance launch 'user data'. Refer to this article for more information http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-windows-user-data.html

cwppolicygroup.py This python script can be used to apply a CWP policy group on a AWS instance. The script automatically finds the AWS instance ID on which this script is executed. You may replace that with the instance ID of another instance. This script also demonstrates the use of 'revoke' policy API call. To get the Policy group ID, navigate in CWP to the policy group details page and copy the policy group ID from the browser URL. E.g. Bm0_7LdATGOLdrwJnnKMTA from the URL sample below https://scwp.securitycloud.symantec.com/webportal/#/cloud/policy-group/view?policyGroupId=Bm0_7LdATGOLdrwJnnKMTA

cwprunavscan.py This script demonstrates the run AV Scan API. This script automatically determines the AWS instance ID where this script is executed. You many specify the instance id of another instance as well. You can run AV scan as 'manual' on demand or as a 'scheduled job'


