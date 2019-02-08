from django.db import models


class Member(models.Model):
    user_role = models.CharField(max_length=10)
    user_id = models.CharField(max_length=30, primary_key=True)
    user_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    businessnum = models.CharField(max_length=30)
    tbc = models.CharField(max_length=30)
    otpkey = models.CharField(max_length=20)
    user_pw = models.CharField(max_length=100)
    c_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user_id


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000 * 5)
    c_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Process(models.Model):
    contract_id = models.CharField(max_length=20)
    OS_hash = models.CharField(max_length=100)
    SR_hash = models.CharField(max_length=100)
    CI_hash = models.CharField(max_length=100)
    LCR_hash = models.CharField(max_length=100)
    LC_hash = models.CharField(max_length=100)
    BL_hash = models.CharField(max_length=100)
    DO_hash = models.CharField(max_length=100)
    user1 = models.CharField(max_length=30)
    user2 = models.CharField(max_length=30)
    user3 = models.CharField(max_length=30)
    user4 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)


class Contract_OS(models.Model):
    contractname = models.CharField(max_length=50)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    item1 = models.CharField(max_length=10)
    item2 = models.CharField(max_length=10, null=True)
    item3 = models.CharField(max_length=10, null=True)
    item4 = models.CharField(max_length=10, null=True)
    item5 = models.CharField(max_length=10, null=True)
    description1 = models.CharField(max_length=30)
    description2 = models.CharField(max_length=30, null=True)
    description3 = models.CharField(max_length=30, null=True)
    description4 = models.CharField(max_length=30, null=True)
    description5 = models.CharField(max_length=30, null=True)
    quantity1 = models.CharField(max_length=20)
    quantity2 = models.CharField(max_length=20, null=True)
    quantity3 = models.CharField(max_length=20, null=True)
    quantity4 = models.CharField(max_length=20, null=True)
    quantity5 = models.CharField(max_length=20, null=True)
    price1 = models.CharField(max_length=20)
    price2 = models.CharField(max_length=20, null=True)
    price3 = models.CharField(max_length=20, null=True)
    price4 = models.CharField(max_length=20, null=True)
    price5 = models.CharField(max_length=20, null=True)
    amount1 = models.CharField(max_length=20)
    amount2 = models.CharField(max_length=20, null=True)
    amount3 = models.CharField(max_length=20, null=True)
    amount4 = models.CharField(max_length=20, null=True)
    amount5 = models.CharField(max_length=20, null=True)


class Contract_LCR(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share3 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    advisingbank = models.CharField(max_length=30)
    applicant = models.CharField(max_length=30)
    beneficiary = models.CharField(max_length=30)
    amount = models.CharField(max_length=20)
    particalshipment = models.CharField(max_length=20)
    transshipment = models.CharField(max_length=20)
    loding = models.CharField(max_length=20)

class Contract_LC(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=30)
    share2 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)

class Contract_SR(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share4 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    consignee = models.CharField(max_length=30)
    notify = models.CharField(max_length=30)
    lport = models.CharField(max_length=30)
    dport = models.CharField(max_length=30)



class Contract_CI(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)

class Contract_BL(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=30)
    share2 = models.CharField(max_length=30)
    share3 = models.CharField(max_length=30)
    status1 = models.CharField(max_length=20)
    status2 = models.CharField(max_length=20)
    status3 = models.CharField(max_length=20)


class Contract_DO(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=30)
    share3 = models.CharField(max_length=30)
    status = models.CharField(max_length=20)