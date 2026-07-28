# 🧑‍🏫 Thomas - AI News Language Tutor

**Thomas** è un tutor linguistico intelligente ed interattivo basato su **Streamlit** e **Google Gemini** (`gemini-3.1-flash-lite`). L'applicazione aiuta gli utenti ad imparare una lingua straniera attraverso notizie locali in tempo reale provenienti da una specifica area geografica, fornendo sia correzioni grammaticali mirate sia la traduzione di supporto.

---

## 🌟 Funzionalità Principali

- **📰 Notizie in Tempo Reale**: Utilizza il *Google Search Grounding* di Gemini per cercare notizie aggiornate sull'area e sugli argomenti scelti dall'utente.
- **📝 Feedback Grammaticale Automatico**: Thomas analizza ogni risposta dell'utente fornendo spiegazioni gentili e correzioni nella lingua madre dell'utente.
- **📊 Calibrazione del Livello**: Contenuti e conversazioni adattati dal livello *Principiante (A1)* fino ad *Avanzato (C1-C2)*.
- **🇬🇧/🇮🇹 Schede con Traduzione Integrata**: La notizia e la conversazione vengono mostrate nella lingua target, con una scheda (Tab) per visualizzare all'occorrenza la traduzione istantanea nella propria lingua madre.
- **🌐 Interfaccia Multilingua Dinamica**: L'intera UI si adatta automaticamente alla lingua madre selezionata (Inglese, Italiano, Spagnolo, Francese, Tedesco, Danese).
- **🪙 Controllo Token & Costi**: La lezione si avvia solo su richiesta dell'utente tramite il pulsante dedicato, evitando chiamate API superflue all'avvio.

---

## 🏗️ Struttura del Progetto

Il progetto segue un'architettura modulare e pulita per facilitare la manutenzione e l'estensione delle funzionalità:

```text
├── main.py                   # Layout principale dell'interfaccia Streamlit e flusso chat
├── utils/
│   ├── __init__.py
│   ├── gemini_helper.py      # Gestione dell'integrazione con Google GenAI API e Search Grounding
│   ├── translations.py       # Dizionario delle traduzioni e mappatura delle lingue/bandiere
│   └── ui_components.py      # Parsing dell'output strutturato e rendering dei messaggi/tab
├── requirements.txt          # Dipendenze Python
└── README.md                 # Documentazione del progetto
