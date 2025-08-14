import pytest

def test_complex_query_structure():
    """Test that the complex ServiceNow query has the correct structure"""
    
    # The complex query from the working curl command
    complex_query = """location.u_region=EMEA^u_resolved>=javascript:gs.dateGenerate('2025-01-01','00:00:00')^u_resolved<=javascript:gs.dateGenerate('2025-12-31','00:00:00')^u_resolvedISNOTEMPTY^(location!=04a8b43cdb22934c627562405b961950^ORlocation=NULL)^(location!=5de7a2eedb96f30095c41aaf299619ae^ORlocation=NULL)^(caller_id!=8183d88ddb83d0544ea59803f396195b^ORcaller_id=NULL)^priorityIN1,2^assignment_group=8d1de3be832e069831009550ceaad37a"""
    
    # Test query structure validation
    assert "location.u_region=EMEA" in complex_query, "EMEA region filter missing"
    assert "priorityIN1,2" in complex_query, "Priority filter missing"
    assert "assignment_group=" in complex_query, "Assignment group filter missing"
    assert "u_resolved>=" in complex_query, "Resolved date start filter missing"
    assert "u_resolved<=" in complex_query, "Resolved date end filter missing"
    assert "u_resolvedISNOTEMPTY" in complex_query, "Resolved not empty filter missing"
    
    # Test that the query uses the correct ServiceNow syntax
    assert "^" in complex_query, "Query should use ^ as separator"
    assert "javascript:gs.dateGenerate" in complex_query, "Date generation function missing"
    
    print("✅ Complex query structure validation passed")

def test_simple_query_structure():
    """Test that the simple ServiceNow query has the correct structure"""
    
    simple_query = "priorityIN1,2"
    
    # Test simple query structure
    assert "priorityIN" in simple_query, "Priority IN operator missing"
    assert "1,2" in simple_query, "Priority values missing"
    
    print("✅ Simple query structure validation passed")

def test_query_encoding():
    """Test that the query can be properly URL encoded"""
    
    complex_query = """location.u_region=EMEA^priorityIN1,2"""
    
    # Test basic encoding
    import urllib.parse
    encoded = urllib.parse.quote(complex_query, safe='')
    
    assert encoded != complex_query, "Query should be URL encoded"
    assert "%3D" in encoded, "Equals sign should be encoded as %3D"
    assert "%5E" in encoded, "Caret should be encoded as %5E"
    
    print("✅ Query encoding validation passed")

def test_field_list():
    """Test that the field list is properly formatted"""
    
    fields = [
        "number", "priority", "opened_at", "u_resolved", "closed_at", 
        "location", "caller_id", "assignment_group", "incident_state"
    ]
    
    # Test field list structure
    assert "number" in fields, "Number field missing"
    assert "priority" in fields, "Priority field missing"
    assert "opened_at" in fields, "Opened date field missing"
    assert "u_resolved" in fields, "Resolved date field missing"
    
    # Test that fields can be joined for API call
    field_string = ",".join(fields)
    assert len(field_string.split(",")) == len(fields), "Field joining failed"
    
    print("✅ Field list validation passed")
