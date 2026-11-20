from pathlib import Path
from io import BytesIO
import json
import joblib
import pandas as pd
import streamlit as st
from reportlab.pdfgen import canvas

ROOT=Path(__file__).parent
DATA=ROOT/'work/source_data/carsdekho.csv'
ART=ROOT/'artifacts'
st.set_page_config(page_title='AutoValue AI',page_icon='🚘',layout='wide')
st.markdown('''<style>
:root{--ink:#132b3b;--muted:#758594;--teal:#12a89c;--orange:#ff9b56}
.stApp{background:#f3f5f6;font-family:'DM Sans',sans-serif;color:var(--ink)}
.block-container{max-width:1420px;padding:1.2rem 2rem 3rem}
[data-testid="stSidebar"]{background:#102838;border-right:1px solid #284251}
[data-testid="stSidebar"] *{color:#eaf3f5!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{padding:.45rem .7rem;border-radius:10px}
.hero{position:relative;overflow:hidden;min-height:260px;padding:34px 40px;border-radius:26px;background:radial-gradient(ellipse at 78% 15%,#2c7883 0%,transparent 36%),linear-gradient(112deg,#102735 0%,#173f4e 57%,#115d65 100%);color:white;box-shadow:0 22px 54px #15394722;margin-bottom:26px}
.hero-copy{position:relative;z-index:2;max-width:58%}
.hero h1{font:800 2.7rem 'Manrope',sans-serif;letter-spacing:-.055em;margin:.35rem 0;color:#fff}
.hero p{font-size:1rem;line-height:1.6;color:#c7dbdc;margin:.2rem 0 1.2rem;max-width:510px}
.eyebrow{font-size:.7rem;text-transform:uppercase;letter-spacing:.2em;color:#77e3cf;font-weight:700}
.hero-chip{display:inline-block;background:#ffffff16;border:1px solid #ffffff2b;border-radius:999px;padding:7px 12px;color:#e6f5f1;font-size:.76rem;margin-right:7px}
.hero-art{position:absolute;width:51%;right:-1%;bottom:-8%;height:105%;opacity:.98}
.section-label{color:#078f87;font-size:.69rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.035em}
div[data-testid="stMetric"]{background:white;border:1px solid #e2e8e8;padding:17px 19px;border-radius:18px;box-shadow:0 10px 30px #203d4a0b}
div[data-testid="stMetricLabel"]{color:#71808b;font-weight:600}
div[data-testid="stMetricValue"]{color:#123646;font-family:'Manrope',sans-serif}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#078d85,#13b09b);border:0;border-radius:12px;padding:.7rem 1.4rem;font-weight:700;box-shadow:0 8px 18px #13a89c30}
div[data-testid="stForm"]{background:#fff;border:1px solid #e2e8e8;padding:22px 24px 18px;border-radius:20px;box-shadow:0 12px 32px #203d4a0a}
div[data-testid="stDataFrame"]{border:1px solid #e1e8e8;border-radius:16px;overflow:hidden}
div[data-testid="stAlert"]{border-radius:14px}
@media(max-width:800px){.block-container{padding:.8rem 1rem 2rem}.hero{padding:25px;min-height:310px}.hero-copy{max-width:100%}.hero h1{font-size:2rem}.hero-art{width:90%;height:48%;right:0;bottom:-6%;opacity:.7}}
</style>''',unsafe_allow_html=True)
df=pd.read_csv(DATA)
meta=json.loads((ART/'metrics.json').read_text())
@st.cache_resource
def load_model(): return joblib.load(ART/'model.joblib')
def money(v): return '₹{:,.0f}'.format(v)
st.markdown('''<div class="hero"><div class="hero-copy"><div class="eyebrow">Your automotive decision studio</div><h1>Drive a smarter<br><span style="color:#77e3cf">deal.</span></h1><p>AI-assisted valuations, vehicle comparisons, and ownership insights, all in one place.</p><span class="hero-chip">✦ Data-led valuations</span><span class="hero-chip">◈ Buyer tools</span></div><svg class="hero-art" viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-label="Stylized premium car illustration"><defs><linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#e8f2ee"/><stop offset=".52" stop-color="#91b7b3"/><stop offset="1" stop-color="#47747b"/></linearGradient><linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#9de3dc" stop-opacity=".85"/><stop offset="1" stop-color="#244858"/></linearGradient><filter id="blur"><feGaussianBlur stdDeviation="15"/></filter></defs><ellipse cx="395" cy="315" rx="270" ry="19" fill="#031924" opacity=".6" filter="url(#blur)"/><path d="M99 259c15-27 44-41 91-51l98-22 86-82c15-14 34-21 56-21h91c32 0 53 12 72 39l49 66c30 9 49 23 58 45l8 29c1 11-8 19-22 19h-37c-6-41-33-65-72-65s-67 24-74 65H286c-7-41-34-65-73-65s-66 24-72 65h-30c-19 0-24-7-22-22z" fill="url(#body)" stroke="#dcf3ed" stroke-width="3"/><path d="m309 178 79-74c10-9 23-14 41-14h45v91z" fill="url(#glass)" stroke="#c4e8e1" stroke-width="3"/><path d="M486 90h33c24 0 39 9 54 28l43 60H486z" fill="url(#glass)" stroke="#c4e8e1" stroke-width="3"/><path d="M393 101v79m93-91v90" stroke="#d6e9e4" stroke-width="4"/><path d="m135 231 90-17m410 1 49 13" stroke="#e8fff6" stroke-width="8" stroke-linecap="round"/><path d="M229 267h56m218 0h76" stroke="#254955" stroke-width="5"/><circle cx="214" cy="268" r="43" fill="#102a37" stroke="#94aaa8" stroke-width="7"/><circle cx="214" cy="268" r="22" fill="#bed3ce"/><circle cx="214" cy="268" r="9" fill="#294957"/><circle cx="583" cy="268" r="43" fill="#102a37" stroke="#94aaa8" stroke-width="7"/><circle cx="583" cy="268" r="22" fill="#bed3ce"/><circle cx="583" cy="268" r="9" fill="#294957"/><path d="M86 305h568" stroke="#65c9b7" stroke-opacity=".4" stroke-width="2"/></svg></div>''',unsafe_allow_html=True)
st.sidebar.markdown('## AUTOVALUE AI')
st.sidebar.caption('USED CAR DECISION STUDIO')
page=st.sidebar.radio('WORKSPACE',['Valuation','Listings','Compare & Budget','Inspection & Costs','Model & Data'])
st.sidebar.markdown('---')
st.sidebar.caption(f"{len(df):,} supplied listings · INR")
stat1,stat2,stat3,stat4=st.columns(4)
stat1.metric('Listings analyzed',f'{len(df):,}')
stat2.metric('Makes covered',f'{df.Make.nunique()}')
stat3.metric('Median listed price',money(df.Price.median()))
stat4.metric('Selected model',meta['selected_model'])
if page=='Valuation':
    st.markdown('<div class="section-label">01 / Valuation</div>',unsafe_allow_html=True)
    st.header('Build your valuation')
    st.write('Choose the vehicle first. The model list updates immediately when you change the maker.')
    a,b=st.columns([1,2])
    make=a.selectbox('Car maker',sorted(df.Make.unique()),key='valuation_make')
    model_options=sorted(df[df.Make==make].Model.unique())
    mod=b.selectbox('Model / variant',model_options,key=f'valuation_model_{make}')
    with st.form('estimate'):
        a,b,c=st.columns(3)
        year=c.number_input('Year',1988,2026,2018)
        a,b,c=st.columns(3)
        km=a.number_input('Kilometres',0,2000000,50000,step=1000)
        fuel=b.selectbox('Fuel',sorted(df['Fuel Type'].unique()))
        trans=c.selectbox('Transmission',sorted(df.Transmission.unique()))
        a,b,c=st.columns(3)
        city=a.selectbox('City',sorted(df.Location.unique()))
        owner=b.selectbox('Owner history',sorted(df.Owner.unique()))
        asking=c.number_input('Asking price (₹)',0,35000000,0,step=10000)
        go=st.form_submit_button('✦  Estimate value',type='primary',use_container_width=True)
    if go:
        r=df[(df.Make==make)&(df.Model==mod)].mode().iloc[0].copy()
        r.update({'Year':year,'Kilometer':km,'Fuel Type':fuel,'Transmission':trans,'Location':city,'Owner':owner})
        for src,dst in [('Engine','Engine CC'),('Max Power','Power BHP'),('Max Torque','Torque Nm')]:
            r[dst]=pd.to_numeric(pd.Series([r[src]]).str.extract(r'(\d+(?:\.\d+)?)')[0],errors='coerce').iloc[0]
        cols=['Make','Model','Fuel Type','Transmission','Location','Owner','Seller Type','Drivetrain','Year','Kilometer','Engine CC','Power BHP','Torque Nm','Length','Width','Height','Seating Capacity','Fuel Tank Capacity']
        pred=float(load_model().predict(pd.DataFrame([r])[cols])[0]); err=meta['empirical_80pct_abs_error']
        st.markdown('<div class="section-label">Your AI valuation</div>',unsafe_allow_html=True)
        m1,m2,m3=st.columns(3)
        m1.metric('Estimated listing value',money(pred)); m2.metric('Indicative range',f'{money(max(0,pred-err))} – {money(pred+err)}'); m3.metric('Model used',meta['selected_model'])
        st.progress(min(1.0,max(.08,1-err/max(pred,1))),text='Indicative estimate confidence (display guide only; range width reflects historical errors)')
        if asking: st.info(('Potentially below estimate' if asking<pred-err*.35 else 'Potentially above estimate' if asking>pred+err*.35 else 'Within broad estimate band')+' · Screen only; verify condition and local listings.')
        st.caption('Range calibrated from held-out absolute errors; uncertainty can be much larger for rare cars.')
        if st.button('Prepare PDF report'):
            buf=BytesIO(); c=canvas.Canvas(buf); c.drawString(60,750,'AutoValue AI — Indicative valuation'); c.drawString(60,720,f'{make} {mod} | {year} | {km:,} km'); c.drawString(60,690,f'Estimate: {money(pred)}'); c.drawString(60,660,f'Empirical range: {money(max(0,pred-err))} – {money(pred+err)}'); c.drawString(60,630,'Historical listing estimate only; not inspection or transaction appraisal.'); c.save(); st.download_button('Download PDF',buf.getvalue(),'autovalue_report.pdf','application/pdf')
elif page=='Listings':
    st.markdown('<div class="section-label">02 / Explore</div>',unsafe_allow_html=True)
    st.header('Browse the listing dataset')
    q=st.text_input('Search make, model, city or fuel')
    lo,hi=st.slider('Price range ₹',0,int(df.Price.max()),(0,int(df.Price.max())),step=50000)
    out=df[df.Price.between(lo,hi)]
    if q: out=out[out.astype(str).apply(lambda col:col.str.contains(q,case=False,na=False)).any(axis=1)]
    st.caption(f'{len(out)} records · listing dates and URLs were not supplied')
    left,right=st.columns([1.2,1])
    with left:
        st.markdown('##### Popular makes in this dataset')
        st.bar_chart(df.Make.value_counts().head(8),horizontal=True,color='#12a89c')
    with right:
        st.markdown('##### Median price by fuel')
        st.bar_chart(df.groupby('Fuel Type').Price.median(),color='#ff9b56')
    st.dataframe(out.head(500),use_container_width=True,hide_index=True)
elif page=='Compare & Budget':
    st.markdown('<div class="section-label">03 / Decide</div>',unsafe_allow_html=True)
    st.header('Compare cars and shortlist')
    budget=st.number_input('Budget ₹',100000,35000000,800000,step=50000)
    c1,c2=st.columns(2); x=c1.selectbox('Car A',sorted(df.Model.unique())); y=c2.selectbox('Car B',sorted(df.Model.unique()),index=1)
    compared=df[df.Model.isin([x,y])].groupby('Model').agg(Count=('Price','size'),Median_price=('Price','median'),Median_year=('Year','median'),Median_km=('Kilometer','median'))
    st.bar_chart(compared['Median_price'],color='#12a89c')
    st.dataframe(compared,use_container_width=True)
    st.write('Listings within budget'); st.dataframe(df[df.Price<=budget].sort_values('Price')[['Make','Model','Year','Kilometer','Fuel Type','Price']].head(20),use_container_width=True,hide_index=True)
elif page=='Inspection & Costs':
    st.markdown('<div class="section-label">04 / Ownership</div>',unsafe_allow_html=True)
    st.header('Plan beyond the purchase price')
    st.warning('Checklist is a rule-based aid, not an AI diagnosis or mechanical inspection.')
    checks=['Engine','Transmission','Suspension','Tyres','Brakes','Accident history','Service records']
    vals=[st.selectbox(k,['Not checked','Pass','Concern'],key=k) for k in checks]
    score=round(sum(10 if v=='Pass' else 5 if v=='Not checked' else 0 for v in vals)/70*100); st.metric('Checklist completion score',f'{score}/100')
    st.caption('Unchecked items receive half credit to represent checklist completion, not vehicle quality.')
    km=st.number_input('Annual km',1000,100000,12000); eff=st.number_input('Fuel efficiency km/l',1.,50.,15.); cost=st.number_input('Fuel ₹/l',1.,300.,105.); maint=st.number_input('Maintenance budget/year ₹',0,1000000,25000)
    st.metric('Scenario annual running cost',money(km/eff*cost+maint))
    price=st.number_input('Current value ₹',50000,35000000,800000); rate=st.slider('Assumed depreciation/year %',0,30,10); years=st.slider('Years ahead',1,10,3)
    st.metric('Scenario value',money(price*(1-rate/100)**years)); st.caption('Constant-rate what-if only; not a forecast.')
else:
    st.markdown('<div class="section-label">05 / Transparency</div>',unsafe_allow_html=True)
    st.header('Model performance and data')
    st.write('Selected model:',meta['selected_model'],'· records:',len(df))
    st.dataframe(pd.DataFrame(meta['metrics']),use_container_width=True,hide_index=True)
    st.caption('One random 80/20 holdout; choice by MAE. Asking prices are not confirmed transaction prices.')
    st.write('Missing values'); st.dataframe(df.isna().sum().to_frame('Missing'))
    st.bar_chart(df.groupby('Fuel Type').Price.median())
    st.info('Source: user-provided CSV; publisher and listing dates unspecified. External datasets reviewed were excluded because market and schema comparability could not be verified.')
