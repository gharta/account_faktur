from odoo import models, api, fields
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class AccountFakturWizard(models.TransientModel):
    _name = "account.faktur.wizard"

    kode_cabang = fields.Char('Kode Cabang (3 Digit)', required=True)
    kode_tahun = fields.Char('Kode Tahun (2 Digit)', required=True)
    nomor_seri_start = fields.Char('Mulai Dari Nomor Seri (8 Digit)', required=True)
    nomor_seri_end = fields.Char('Sampai Nomor Seri (8 Digit)', required=True)

    @api.one
    @api.constrains('kode_cabang', 'kode_tahun', 'nomor_seri_start', 'nomor_seri_end')
    def _check_format(self):
        # xxx-xx-xxxxxxxx
        if self.kode_cabang:
            if not (len(self.kode_cabang) == 3 and self.kode_cabang.isdigit()):
                raise ValidationError("Kode Cabang harus 3 Digit Angka!")
        if self.kode_tahun:
            if not (len(self.kode_tahun) == 2 and self.kode_tahun.isdigit()):
                raise ValidationError("Kode Tahun harus 2 Digit Angka!")
        if self.nomor_seri_start:
            if not (len(self.nomor_seri_start) == 8 and self.nomor_seri_start.isdigit()):
                raise ValidationError("Nomor Seri harus 8 Digit Angka!")
        if self.nomor_seri_end:
            if not (len(self.nomor_seri_end) == 8 and self.nomor_seri_end.isdigit()):
                raise ValidationError("Nomor Seri harus 8 Digit Angka!")
        if self.nomor_seri_end and self.nomor_seri_start:
            if self.nomor_seri_end <= self.nomor_seri_start:
                raise ValidationError("Nomor Seri harus dari yang lebih kecil ke besar!")

    @api.one
    def action_generate_account_faktur(self):
        int_nomor_seri_start = int(self.nomor_seri_start) #1000
        int_nomor_seri_end = int(self.nomor_seri_end) #1100
        int_nomor_seri = int_nomor_seri_start #1000 disimpan di var
        while int_nomor_seri <= int_nomor_seri_end: #selama var < 1100
            # Create
            self.env['account.faktur'].create({
                'name' : self.kode_cabang + '-' + self.kode_tahun + '-' + str(int_nomor_seri) 
            })
            int_nomor_seri = int_nomor_seri + 1 #var = var + 1
        