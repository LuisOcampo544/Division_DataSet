import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from sklearn.model_selection import train_test_split
import arff   # liac-arff

# --- helpers ---
def fig_to_base64():
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def load_kdd_dataset_from_fileobj(file_obj):
    """
    file_obj: archivo subido (InMemoryUploadedFile o similar)
    devuelve: pandas.DataFrame
    """
    # liac-arff espera texto; file_obj puede ser bytes buffer
    # convertimos a str si viene como bytes
    try:
        # file_obj.read() puede consumir el stream, por eso guardamos contenido
        raw = file_obj.read()
        # if bytes -> decode, else assume str
        if isinstance(raw, bytes):
            raw_str = raw.decode('utf-8', errors='ignore')
        else:
            raw_str = raw
        parsed = arff.loads(raw_str)
        attributes = [a[0] for a in parsed['attributes']]
        data = parsed['data']
        df = pd.DataFrame(data, columns=attributes)
        return df
    finally:
        try:
            file_obj.seek(0)
        except Exception:
            pass

# --- vista ---
def upload_file(request):
    graphs = []
    columns = []
    rows = 0

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded = request.FILES['file']

        # cargar DataFrame desde .arff subido
        df = load_kdd_dataset_from_fileobj(uploaded)

        # info básica
        columns = df.columns.tolist()
        rows = len(df)

        # dividir 60/40
        train_set, test_set = train_test_split(df, test_size=0.4, random_state=42)

        # ---------- 1) Distribución de clases (si existe última columna de clase) ----------
        # intentamos detectar columna etiqueta: por nombre común o asumimos última columna
        label_col = None
        for cand in ['class', 'label', 'attack', 'tipo', 'tipo_atq']:
            if cand in df.columns:
                label_col = cand
                break
        if label_col is None:
            # tomar la última columna por defecto
            label_col = df.columns[-1]

        try:
            plt.figure(figsize=(6,4))
            df[label_col].value_counts().plot(kind='bar')
            plt.title('Distribución de clases (' + str(label_col) + ')')
            plt.xlabel('Clase')
            plt.ylabel('Frecuencia')
            graphs.append(fig_to_base64())
        except Exception:
            # si falla (p.ej. columna no categórica), añadimos placeholder vacío
            graphs.append(None)

        # ---------- 2) Matriz de correlación (solo numéricas) ----------
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        if not numeric_df.empty:
            try:
                plt.figure(figsize=(6,5))
                plt.imshow(numeric_df.corr(), interpolation='nearest', aspect='auto')
                plt.title('Correlación entre variables numéricas')
                plt.colorbar()
                graphs.append(fig_to_base64())
            except Exception:
                graphs.append(None)
        else:
            graphs.append(None)

        # ---------- 3) Histograma de la primera variable numérica (si existe) ----------
        if not numeric_df.empty:
            try:
                plt.figure(figsize=(6,4))
                col0 = numeric_df.columns[0]
                numeric_df[col0].hist(bins=30)
                plt.title(f'Distribución de {col0}')
                graphs.append(fig_to_base64())
            except Exception:
                graphs.append(None)
        else:
            graphs.append(None)

        # ---------- 4) Proporción Train/Test (barras) ----------
        try:
            plt.figure(figsize=(5,4))
            plt.bar(['Train', 'Test'], [len(train_set), len(test_set)])
            plt.title('Tamaño de conjuntos (Train vs Test)')
            graphs.append(fig_to_base64())
        except Exception:
            graphs.append(None)

    context = {
        'graphs': graphs,
        'columns': columns,
        'rows': rows,
    }
    return render(request, 'upload.html', context)
