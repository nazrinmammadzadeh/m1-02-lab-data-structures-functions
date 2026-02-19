#  TASK 2:

def validate_required_keys(records, required_keys):
    """
    Identifies records that are missing one or more required keys.
    Returns a list of dictionaries that failed the check.
    """
    invalid_records = []
    
    for record in records:
        # Check if all required keys exist in the current record
        if not all(key in record for key in required_keys):
            invalid_records.append(record)
            
    return invalid_records

def get_invalid_resolution_records(records):
    """
    Identifies records where resolution_minutes is not a valid number.
    Returns a list of indices (positions) of the bad records.
    """
    bad_indices = []
    
    for index, record in enumerate(records):
        val = record.get("resolution_minutes")
        
        # Check if the value is missing (None) or not an integer
        if val is None or not isinstance(val, int):
            bad_indices.append(index)
            
    return bad_indices


# ----------------------

# TASK 3:
def clean_ticket_data(records, default_res=0):
    """
    Returns a new list of cleaned records.
    - Normalizes category strings (lowercase + strip).
    - Repairs resolution_minutes by replacing non-ints with a default value.
    """
    cleaned_list = []
    
    for record in records:
        # Create a copy to avoid mutating the original dictionary
        clean_rec = record.copy()
        
        # 1. Normalize Category
        if isinstance(clean_rec.get("category"), str):
            clean_rec["category"] = clean_rec["category"].strip().title()
            
        # 2. Repair Resolution Minutes
        res_val = clean_rec.get("resolution_minutes")
        if not isinstance(res_val, int):
            clean_rec["resolution_minutes"] = default_res
            
        cleaned_list.append(clean_rec)
        
    return cleaned_list


# ----------------------------

# TASK 4:

def get_avg_resolution_by_category(records):
    """Returns a dictionary: {category: avg_minutes}"""
    totals = {} # {category: [sum_mins, count]}
    
    for rec in records:
        cat = rec['category']
        mins = rec['resolution_minutes']
        
        if cat not in totals:
            totals[cat] = [0, 0]
        
        totals[cat][0] += mins
        totals[cat][1] += 1
    
    # Calculate averages: sum / count
    return {cat: (val[0] / val[1]) for cat, val in totals.items()}


def get_ticket_count_per_customer(records):
    """Returns a dictionary: {customer_id: ticket_count}"""
    customer_counts = {}
    
    for rec in records:
        cust_id = rec['customer_id']
        customer_counts[cust_id] = customer_counts.get(cust_id, 0) + 1
        
    return customer_counts


def get_escalation_metrics(records):
    """Returns a dict with 'overall' rate and a nested dict for 'by_category'"""
    cat_stats = {} # {category: [escalated_count, total_count]}
    overall_escalated = 0
    
    for rec in records:
        cat = rec['category']
        is_esc = rec['escalated']
        
        if is_esc:
            overall_escalated += 1
            
        if cat not in cat_stats:
            cat_stats[cat] = [0, 0]
        
        if is_esc:
            cat_stats[cat][0] += 1
        cat_stats[cat][1] += 1
        
    # Formatting results
    results = {
        "overall": overall_escalated / len(records),
        "by_category": {cat: (vals[0] / vals[1]) for cat, vals in cat_stats.items()}
    }
    return results



# TASK 5:

def generate_final_report(records):
    """
    Consolidates all analysis metrics into a single nested dictionary.
    """
    report = {
        "metadata": {
            "total_tickets": len(records),
            "status": "Cleaned & Verified"
        },
        "averages": get_avg_resolution_by_category(records),
        "escalation_stats": get_escalation_metrics(records),
        "customer_activity": {
            "unique_customers": len(get_ticket_count_per_customer(records)),
            # We can find the top customer for extra insight
            "top_customer": max(get_ticket_count_per_customer(records), 
                                key=get_ticket_count_per_customer(records).get)
        }
    }
    return report