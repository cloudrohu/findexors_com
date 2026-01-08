from business.models import Company
from collections import defaultdict

data = defaultdict(list)

# saare contact number collect karo
for c in Company.objects.exclude(contact_no__isnull=True).exclude(contact_no=""):
    data[c.contact_no].append(c)

# duplicate ko auto-fix karo
for number, companies in data.items():
    if len(companies) > 1:
        for company in companies[1:]:
            company.contact_no = f"{number}_{company.id}"
            company.save()
            print("Fixed:", company.id, company.contact_no)

print("DONE")
