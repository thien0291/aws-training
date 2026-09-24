# Fix: Glue Permissions Error in Lab 05

## Error Message
```
GENERIC_INTERNAL_ERROR: Forbidden: User: arn:aws:sts::327843408678:assumed-role/datazone_usr_role_6pgc0tmnmwcopz_cfbs3v1oh35i5j/04984448-2041-7054-577e-653c1635853e@cfbs3v1oh35i5j 
is not authorized to perform: glue:GetTable on resource: arn:aws:glue:us-east-1:327843408678:database/rms-catalog/zetl_bdb1cad7-afba-43be-915d-96afb0cd7829/fsidb 
because no identity-based policy allows the glue:GetTable action
```

## Root Cause
The DataZone user role (`datazone_usr_role_*`) doesn't have permissions to access AWS Glue catalog resources for the Zero-ETL replicated database. This role is automatically created by SageMaker Unified Studio/DataZone but needs additional permissions to query Zero-ETL tables.

## Solution: Add Glue Permissions to DataZone User Role

### Step 1: Identify the DataZone User Role

1. Go to **IAM Console** → **Roles**
2. Search for roles starting with `datazone_usr_role_`
3. You should see a role like: `datazone_usr_role_6pgc0tmnmwcopz_cfbs3v1oh35i5j`
4. Click on the role name to open it

### Step 2: Add Inline Policy for Glue Permissions

1. In the role details page, click the **Permissions** tab
2. Click **Add permissions** → **Create inline policy**
3. Click the **JSON** tab
4. Paste the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "GlueCatalogAccess",
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabase",
                "glue:GetDatabases",
                "glue:GetTable",
                "glue:GetTables",
                "glue:GetPartition",
                "glue:GetPartitions",
                "glue:BatchGetPartition"
            ],
            "Resource": [
                "arn:aws:glue:*:*:catalog",
                "arn:aws:glue:*:*:database/rms-catalog/*",
                "arn:aws:glue:*:*:database/zetl_*",
                "arn:aws:glue:*:*:table/rms-catalog/*/*",
                "arn:aws:glue:*:*:table/zetl_*/*/*"
            ]
        },
        {
            "Sid": "RedshiftDataAccess",
            "Effect": "Allow",
            "Action": [
                "redshift-data:ExecuteStatement",
                "redshift-data:DescribeStatement",
                "redshift-data:GetStatementResult",
                "redshift-data:ListDatabases",
                "redshift-data:ListSchemas",
                "redshift-data:ListTables"
            ],
            "Resource": "*"
        },
        {
            "Sid": "RedshiftServerlessAccess",
            "Effect": "Allow",
            "Action": [
                "redshift-serverless:GetCredentials",
                "redshift-serverless:GetWorkgroup",
                "redshift-serverless:GetNamespace"
            ],
            "Resource": "*"
        }
    ]
}
```

5. Click **Next**
6. Name the policy: `GlueZeroETLAccess`
7. Click **Create policy**

### Step 3: Verify the Fix

1. Go back to **SageMaker Unified Studio**
2. Navigate to **Query Editor**
3. Try running the query from Lab 05 again:

```sql
select '1. Assets' as Tablename,count(*) as Count from fsidb.assets union
select '2. Maintenance',count(*) from fsidb.maintenance union
select '3. Operations', count(*) from fsidb.operations order by 1;
```

The query should now execute successfully.

## Alternative Solution: Use Lake Formation Permissions

If the above solution doesn't work, you may need to grant Lake Formation permissions:

### Step 1: Go to Lake Formation Console

1. Navigate to **AWS Lake Formation** console
2. Click **Permissions** → **Data lake permissions**

### Step 2: Grant Database Permissions

1. Click **Grant**
2. Under **Principals**, select **IAM users and roles**
3. Search for and select the `datazone_usr_role_*` role
4. Under **LF-Tags or catalog resources**, select **Named data catalog resources**
5. Under **Databases**, select the Zero-ETL database (starts with `zetl_`)
6. Under **Database permissions**, select:
   - Describe
7. Under **Grantable permissions**, leave unchecked
8. Click **Grant**

### Step 3: Grant Table Permissions

1. Click **Grant** again
2. Under **Principals**, select the same `datazone_usr_role_*` role
3. Under **LF-Tags or catalog resources**, select **Named data catalog resources**
4. Under **Databases**, select the Zero-ETL database
5. Under **Tables**, select **All tables**
6. Under **Table permissions**, select:
   - Select
   - Describe
7. Click **Grant**

## Prevention: Add to CloudFormation Template

To prevent this issue in future deployments, add the Glue permissions policy to the CloudFormation template that creates the DataZone domain/project.

Add this to the IAM role resource:

```yaml
DataZoneUserRolePolicy:
  Type: AWS::IAM::Policy
  Properties:
    PolicyName: GlueZeroETLAccess
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Sid: GlueCatalogAccess
          Effect: Allow
          Action:
            - glue:GetDatabase
            - glue:GetDatabases
            - glue:GetTable
            - glue:GetTables
            - glue:GetPartition
            - glue:GetPartitions
            - glue:BatchGetPartition
          Resource:
            - !Sub 'arn:aws:glue:*:${AWS::AccountId}:catalog'
            - !Sub 'arn:aws:glue:*:${AWS::AccountId}:database/rms-catalog/*'
            - !Sub 'arn:aws:glue:*:${AWS::AccountId}:database/zetl_*'
            - !Sub 'arn:aws:glue:*:${AWS::AccountId}:table/rms-catalog/*/*'
            - !Sub 'arn:aws:glue:*:${AWS::AccountId}:table/zetl_*/*/*'
    Roles:
      - !Ref DataZoneUserRole
```

## Troubleshooting

### Issue: Still getting permission errors after adding policy

**Check:**
1. Verify you added the policy to the correct role (the one in the error message)
2. Wait 1-2 minutes for IAM policy changes to propagate
3. Refresh your SageMaker Unified Studio browser tab
4. Try the query again

### Issue: Can't find the datazone_usr_role

**Solution:**
1. Look at the error message - it contains the exact role name
2. Copy the role name from the error: `datazone_usr_role_6pgc0tmnmwcopz_cfbs3v1oh35i5j`
3. Search for it in IAM Console

### Issue: Multiple datazone_usr_role roles exist

**Solution:**
- Each SageMaker domain/project may have its own role
- Add the policy to all roles that start with `datazone_usr_role_`
- Or identify the specific role from the error message

## Summary

This error occurs because DataZone user roles don't automatically get Glue catalog permissions for Zero-ETL databases. The fix is to add an inline policy granting the necessary Glue permissions to the DataZone user role.

**Quick Fix Steps:**
1. Find the `datazone_usr_role_*` in IAM
2. Add inline policy with Glue permissions (see JSON above)
3. Retry the query in SageMaker Unified Studio

This should resolve the `glue:GetTable` permission error in Lab 05.
