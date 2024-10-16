import pandas as pd

# Читаем первые n строк
n = 2000

df = pd.read_excel('Medicine_description.xlsx', sheet_name='Sheet1', header=0, nrows=n)

# Получаем уникальные значения из столбца Reason (Причина)
reasons = df["Reason"].unique()

# Присваиваем номер каждой причине
reasons_dict = {reason: i for i, reason in enumerate(reasons)}

# Добавляем символ новой строки и ### в конец каждого описания
df["Drug_Name"] = "Drug: " + df["Drug_Name"] + "\n" + "Malady:"

df["Reason"] = " " + df["Reason"].apply(lambda x: "" + str(reasons_dict[x]))

# Удаляем столбец Description
df.drop(["Description"], axis=1, inplace=True)

# Переименовываем столбцы
df.rename(columns={"Drug_Name": "prompt", "Reason": "completion"}, inplace=True)

# Конвертируем кадр данных в формат JSONL
jsonl = df.to_json(orient="records", indent=0, lines=True)

# Записываем jsonl в файл
with open("drug_malady_data.jsonl", "w") as f:
    f.write(jsonl)
