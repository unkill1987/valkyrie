from django.db import models



# Create your models here.


class Member(models.Model):
    user_role = models.CharField(max_length=20)
    user_id = models.CharField(max_length=30, primary_key=True)
    user_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    otpkey = models.CharField(max_length=20)
    user_pw = models.CharField(max_length=50)
    c_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user_id


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000*5)
    c_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Process(models.Model):
    contract_id = models.CharField(max_length=20)
    CI_hash = models.CharField(max_length=100)
    SR_hash = models.CharField(max_length=100)
    LCR_hash = models.CharField(max_length=100)
    LC_hash = models.CharField(max_length=100)
    BL_hash = models.CharField(max_length=100)
    DO_hash = models.CharField(max_length=100)
    user1 = models.CharField(max_length=50)
    user2 = models.CharField(max_length=50)
    user3 = models.CharField(max_length=50)
    user4 = models.CharField(max_length=50)


class Contract_LCR(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)


class Contract_LC(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)


class Contract_CI(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)


class Contract_SR(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)


class Contract_BL(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)


class Contract_DO(models.Model):
    contractname = models.CharField(max_length=50)
    contract_id = models.CharField(max_length=20)
    sha256 = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    share1 = models.CharField(max_length=100)
    share2 = models.CharField(max_length=100)
    share3 = models.CharField(max_length=100)
    share4 = models.CharField(max_length=100)