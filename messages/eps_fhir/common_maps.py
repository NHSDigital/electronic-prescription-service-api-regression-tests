INTENT_MAP = {"acute": "order", "repeat": "instance-order", "eRD": "original-order"}

THERAPY_TYPE_MAP = {
    "acute": {"code": "acute", "display": "Short course (acute) therapy"},
    "repeat": {"code": "continuous", "display": "Continuous long term therapy"},
    "eRD": {
        "code": "continuous-repeat-dispensing",
        "display": "Continuous long term (repeat dispensing)",
    },
}

STATUS_MAP = {
    "Awaiting Release Ready": "0000",
    "To be Dispensed": "0001",
    "With Dispenser": "0002",
    "With Dispenser - Active": "0003",
    "Expired": "0004",
    "Cancelled": "0005",
    "Dispensed": "0006",
    "Not Dispensed": "0007",
    "Claimed": "0008",
    "No-Claimed": "0009",
    "Repeat Dispense future instance": "9000",
    "Prescription future instance": "9001",
    "Cancelled future instance": "9005",
}


LINE_ITEM_STATUS_MAP = {
    "Item fully dispensed": "0001",
    "Item not dispensed": "0002",
    "Item dispensed - partial": "0003",
    "Item not dispensed - owing": "0004",
    "Item Cancelled": "0005",
    "Expired": "0006",
    "Item to be dispensed": "0007",
    "Item with dispenser": "0008",
}

NON_DISPENSING_REASON_MAP = {
    "Not required as instructed by the patient": "0001",
    "Clinically unsuitable": "0002",
    "Owings note issued to patient": "0003",
    "Prescription cancellation": "0004",
    "Prescription cancellation due to death": "0005",
    "Illegal NHS prescription": "0006",
    "Prescribed out of scope item": "0007",
    "Item or prescription expired": "0008",
    "Not allowed on FP10": "0009",
    "Patient did not collect medication": "0010",
    "Patient purchased medication over the counter": "0011",
}

CANCELLATION_REASON_MAP = {
    "Prescribing Error": "0001",
    "Clinical contra-indication": "0002",
    "Change to medication treatment regime": "0003",
    "Clinical grounds": "0004",
    "At the Patients request": "0005",
    "At the Pharmacists request": "0006",
    "Notification of Death": "0007",
    "Patient deducted - other reason": "0008",
    "Patient deducted - registered with new practice": "0009",
}
