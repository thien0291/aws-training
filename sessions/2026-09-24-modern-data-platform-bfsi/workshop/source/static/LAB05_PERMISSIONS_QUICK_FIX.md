# Lab 05 Permissions Error - Quick Fix

## Error Message
```
GENERIC_INTERNAL_ERROR: Forbidden: User: arn:aws:sts::ACCOUNT:assumed-role/datazone_usr_role_*/USER 
is not authorized to perform: glue:GetTable on resource: arn:aws:glue:REGION:ACCOUNT:database/rms-catalog/zetl_*/fsidb 
because no identity-based policy allows the glue:GetTable action
```

## Quick Fix (Automated)

Run this command in AWS CloudShell or your terminal:

```bash
curl -O https://raw.githubusercontent.com/YOUR_REPO/main/static/fix_glue_permissions_cli.sh
chmod +x fix_glue_permissions_cli.sh
./fix_glue_permissions_cli.sh
```

## Manual Fix (5 minutes)

1. **Go to IAM Console** → Roles
2. **Search for** `datazone_usr_role_` (find the role with your domain ID)
3. **Click** the role name
4. **Click** "Add permissions" → "Create inline policy"
5. **Switch to JSON** tab
6. **Paste this policy**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabase",
                "glue:GetDatabases",
                "glue:GetTable",
                "glue:GetTables",
                "glue:GetPartition",
                "glue:GetPartitions"
            ],
            "Resource": [
                "arn:aws:glue:*:*:catalog",
                "arn:aws:glue:*:*:database/rms-catalog/*",
                "arn:aws:glue:*:*:database/zetl_*",
                "arn:aws:glue:*:*:table/rms-catalog/*/*",
                "arn:aws:glue:*:*:table/zetl_*/*/*"
            ]
        }
    ]
}
```

7. **Name the policy**: `GlueZeroETLAccess`
8. **Click** "Create policy"
9. **Return to Lab 05** and retry your query

## Verify Fix

Run this query in SageMaker Query Editor:

```sql
SELECT * FROM fsidb.assets LIMIT 5;
```

If you see results, the fix worked! ✅

## Need More Help?

See the detailed guide: [fix_glue_permissions.md](fix_glue_permissions.md)
