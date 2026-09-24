#!/bin/bash

# ============================================================================
# Fix Glue Permissions for DataZone User Role - CLI Script
# ============================================================================
# This script adds the necessary Glue permissions to the DataZone user role
# to fix the "glue:GetTable" permission error in Lab 05.
#
# Usage:
#   1. Make the script executable: chmod +x fix_glue_permissions_cli.sh
#   2. Run: ./fix_glue_permissions_cli.sh <role-name>
#   
# Example:
#   ./fix_glue_permissions_cli.sh datazone_usr_role_6pgc0tmnmwcopz_cfbs3v1oh35i5j
#
# Or to auto-detect and fix all datazone_usr_role roles:
#   ./fix_glue_permissions_cli.sh --all
# ============================================================================

set -e

POLICY_NAME="GlueZeroETLAccess"
POLICY_FILE="add_glue_permissions_policy.json"

# Check if policy file exists
if [ ! -f "$POLICY_FILE" ]; then
    echo "Error: Policy file '$POLICY_FILE' not found!"
    echo "Please ensure add_glue_permissions_policy.json is in the current directory."
    exit 1
fi

# Function to add policy to a role
add_policy_to_role() {
    local role_name=$1
    
    echo "Adding policy '$POLICY_NAME' to role '$role_name'..."
    
    aws iam put-role-policy \
        --role-name "$role_name" \
        --policy-name "$POLICY_NAME" \
        --policy-document file://"$POLICY_FILE"
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully added policy to role: $role_name"
    else
        echo "❌ Failed to add policy to role: $role_name"
        return 1
    fi
}

# Main logic
if [ "$1" == "--all" ]; then
    echo "Finding all datazone_usr_role roles..."
    
    # Get all roles starting with datazone_usr_role
    roles=$(aws iam list-roles --query 'Roles[?starts_with(RoleName, `datazone_usr_role`)].RoleName' --output text)
    
    if [ -z "$roles" ]; then
        echo "No datazone_usr_role roles found."
        exit 1
    fi
    
    echo "Found roles:"
    echo "$roles"
    echo ""
    
    # Add policy to each role
    for role in $roles; do
        add_policy_to_role "$role"
        echo ""
    done
    
    echo "✅ All roles updated successfully!"
    
elif [ -z "$1" ]; then
    echo "Usage: $0 <role-name>"
    echo "   or: $0 --all"
    echo ""
    echo "Example:"
    echo "  $0 datazone_usr_role_6pgc0tmnmwcopz_cfbs3v1oh35i5j"
    echo "  $0 --all"
    exit 1
    
else
    ROLE_NAME=$1
    
    # Check if role exists
    aws iam get-role --role-name "$ROLE_NAME" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Role '$ROLE_NAME' not found!"
        exit 1
    fi
    
    add_policy_to_role "$ROLE_NAME"
fi

echo ""
echo "🎉 Done! Users should now be able to query Zero-ETL tables in Lab 05."
echo "   Note: IAM policy changes may take 1-2 minutes to propagate."
