import pdfplumber
import glob
import csv

axis_cc_dir = "/Users/sonu-14757/Downloads/axis/*"
icici_cc_dir = "/Users/sonu-14757/Downloads/icici/*"
hdfc_cc_dir = "/Users/sonu-14757/Downloads/hdfc/*"
paytm_sb_dir = "/Users/sonu-14757/Downloads/paytm/*"
hdfc_sb_dir = "/Users/sonu-14757/Downloads/hdfc_sb/*"

fields = ['DATE','DESCRIPTION','DEBIT','CREDIT','ACCOUNT','TYPE']
output_file = '/Users/sonu-14757/Desktop/consolidated.csv'
output_csv = []
    
# ============================ HDFC BANK STATEMENT ============================

hdfc_sb_stmts = glob.glob(hdfc_sb_dir)
for stmt in hdfc_sb_stmts:
    with open(stmt, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if(len(row) == 7 and row[0].strip() != 'Date'):
                dummy = [row[0].strip(),row[1].strip(),0,0,'HDFC 6760', 'SAVINGS ACCOUNT']
                if(row[3].strip() != '0.00'):
                    dummy[2] = float(row[3].strip())
                elif(row[4].strip() != '0.00'):
                    dummy[3] = float(row[4].strip())
                # print(dummy)
                output_csv.append(dummy)

# ============================ PAYTM BANK STATEMENT ============================

paytm_sb_stmts = glob.glob(paytm_sb_dir)
for stmt in paytm_sb_stmts:
    with open(stmt, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if(len(row) == 12 and 'Date' not in row[1]):
                dummy = [row[1].split(' ')[0].replace('-','/'),'',0,0,'PAYTM 4110','SAVINGS ACCOUNT']
                if(row[4] == 'C'):
                    dummy[3] = round(float(row[3]),2)
                    if('Interest Received' in row[2]):
                        dummy[1] = 'Interest Received'
                    elif('Restored against Failed Payment' in row[2]):
                        dummy[1] = 'Restored against Failed Payment'
                    elif('Refund received' in row[2]):
                        dummy[1] = 'Refund ' + row[2].split('\n')[1].strip()
                    # elif(row[10] == ''):
                        # print(row)
                    else:
                        if(row[10] == ''):
                            dummy[1] = row[2].split('\n')[0].strip()
                        else:
                            dummy[1] = row[10]
                elif(row[4] == 'D'):
                    dummy[2] = float(row[3])
                    if('Paid online using debit card' in row[2]):
                        dummy[1] = 'Debit Card - ' + row[2].split('\n')[1].strip()
                    elif('Debit Card Annual Charges' in row[2]):
                        dummy[1] = 'Debit Card Annual Charges'
                    elif(row[8] == ''):
                      dummy[1] = row[2].split('\n')[0].strip()
                    else:
                        if(row[8] == ''):
                            dummy[1] = row[2].split('\n')[0].strip()
                        else:
                            dummy[1] = row[8]
                # print(dummy)
                output_csv.append(dummy)

# # ============================ HDFC CREDIT CARD STATEMENT ============================

hdfc_cc_stmts = glob.glob(hdfc_cc_dir)
for stmt in hdfc_cc_stmts:
    pdf = pdfplumber.open(stmt, password = 'SONU1512')
    pages = pdf.pages
    for page in pages:
        table = page.extract_table()
        for row in table:
            if(len(row) == 4):
                if(row[0] != None and '/20' in row[0]):
                    if('null' in row[0]):
                        row[0] = row[0].split(' ')[1]
                    dummy = [row[0],row[1],0,0,'HDFC 5455','CREDIT CARD']
                    if('Cr' in row[2]):
                        dummy[3] = float(row[2].split('Cr')[0].replace(',',''))
                    else:
                        dummy[2] = float(row[2].replace(',',''))
                    # print(dummy)
                    output_csv.append(dummy)

# # ============================ ICICI CREDIT CARD STATEMENT ============================

icici_cc_stmts = glob.glob(icici_cc_dir)
for stmt in icici_cc_stmts:
    with open(stmt, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if(len(row) == 7):
                dummy = [row[0],row[2],0,0,'ICICI 3002','CREDIT CARD']
                if(row[-1] == ''):
                    dummy[2] = float(row[-2])
                elif(row[-1] == 'CR'):
                    dummy[3] = float(row[-2])
                else:
                    continue
                # print(dummy)
                output_csv.append(dummy)

# # ============================ AXIS CREDIT CARD STATEMENT ============================

axis_cc_stmts = glob.glob(axis_cc_dir)
for stmt in axis_cc_stmts:
    pdf = pdfplumber.open(stmt, password = 'SONU1512')
    pages = pdf.pages

    isFirstPage = True
    for page in pages[:-1]:
        if(isFirstPage):
            table = page.extract_table()[3:-1]
            isFirstPage = False
        else:
            table = page.extract_table()[1:-1]

        for row in table:
            dummy = [row[0],row[1],0,0,'AXIS 0189','CREDIT CARD']
            if('Cr' in row[-2]):
                dummy[3] = float(row[-2].strip(' Cr').replace(',',''))
            elif('Dr' in row[-2]):
                dummy[2] = float(row[-2].strip(' Dr').replace(',',''))
            # print(dummy)
            output_csv.append(dummy)
    # print()

with open(output_file, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(output_csv) 