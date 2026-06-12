
import streamlit as st
import google.generativeai as genai
import requests
import xml.etree.ElementTree as ET
import json


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


def general_agent(disease,target):
  prompt = f"""
  You are a drug discovery expert
  Disease:{disease}
  Target:{target}
  Explain:
  1. Disease Mechanism
  2.Current treatments
  3.Unmet clinical needs

  1. Biological Function of Target
  2. Disease Relevance of Target
  3. Druggability of Target

  Use clear Headings.
  Suggest:
  1. Drug discovery strategy
  2. Opportunities
  3. Challenges
  4. Future Directions

  Use clear Headings.
  """
  response = model.generate_content(prompt)
  return response.text

def risk_agent(disease, target):

    prompt = f"""
    You are a drug discovery scientist
    Disease: {disease}
    Target: {target}

    Evaluate the target and return ONLY valid JSON.
    Requirements:
    -Scores must be integers between 0 to 100
    -Do not provide explanations.
    -Do not provide reasonings.
    -Do not provide text descriptions.
    -Return JSON only.

    Format:

    {{
      "Biological_evidence":0,
      "Druggability":0,
      "clinical_validation":0,
      "safety_risk":0,
      "Novelty":0,
    }}
    """

    response = model.generate_content(prompt)

    text = response.text


    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)

def get_status(score):
  if score>=70:
    return "🟢 Proceed to Validation "
  elif score>=40:
    return "🟡 Requires Further Research"
  else:
    return "🔴 Not Recommended Currently"
def get_recommendation(score):

  if score >= 70:
     return "🟢 Proceed to Validation"

  elif score >= 40:
     return "🟡 Requires Further Research"

  else:
    return "🔴 Not Recommended Currently"

def search_pubmed(query):

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={query} &retmax=5&retmode=json"
    )

    response = requests.get(url)

    return response.json()

def get_paper_titles(id_list):

    ids = ",".join(id_list)

    url =(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"efetch.fcgi?db=pubmed&id={ids}&retmode=xml"
        )
    response = requests.get(url)
    root =ET.fromstring(response.content)
    titles = []
    for article in root.findall(".//ArticleTitle"):
      titles.append(article.text)
    return titles

print("TOP PAPERS")

def research_gap_agent(titles_text):

    prompt = f"""
    You are a drug discovery expert.

    Based on these publications:

    {titles_text}

    Identify:

    1. Research gaps
    2. Challenges
    3. Future opportunities

    Keep it concise.
    """

    response = model.generate_content(prompt)

    return response.text

def recommendation_agent(
    disease,
    target,
    risk_data,
    research_gap_output
):

    prompt = f"""
    Disease: {disease}

    Target: {target}

    Risk Assessment:
    {risk_data}

    Research Gaps:
    {research_gap_output}

    Provide:

    1. Target Priority
    2. Key Strengths
    3. Major Risks
    4. Recommended Next Step

    Keep under 200 words.
    """

    response = model.generate_content(prompt)

    return response.text

st.title("Drug Discovery Research Copilot")
st.write(
    "AI-powered platform for target assessment, literature mining, and research gap identification.")

disease = st.text_input("Disease")
target = st.text_input("Target")

if st.button("Analyze"):
  general_Analysis = general_agent(disease, target)

  risk_data = risk_agent(disease, target)
  overall_score =(
        risk_data["Biological_evidence"] +
        risk_data["Druggability"] +
        risk_data["clinical_validation"] +
        risk_data["safety_risk"] +
        risk_data["Novelty"]
    )/5
  risk_data["overall_score"] = round(overall_score)
  recommendation = get_recommendation(risk_data["overall_score"])

  query = f"{disease} {target}"
  results = search_pubmed(query)
  paper_ids = results.get("esearchresult",{}).get("idlist",[])
  if not paper_ids:
    st.error("No papers found for the given query.")
    st.stop()

  titles = get_paper_titles(paper_ids)


  titles_text = "\n".join(titles)
  for i,title in enumerate(titles,1):
      print(f"{i}.{title}")

  titles_text = "\n".join(titles)

  research_gap_output = research_gap_agent(titles_text)


  recommendation = recommendation_agent(
          disease,
          target,
          risk_data,
          research_gap_output
      )
  st.subheader("General Analysis")
  st.write(general_Analysis)
  st.subheader("Risk Assessment")
  for metric,score in risk_data.items():
    if metric == "overall_score":
      continue
    st.write(
        f"{metric}: {get_status(score)} {score}/100"
    )
  st.subheader("Overall Score")
  st.write(f"{risk_data['overall_score']}/100")
  st.write(
          f"Overall Status: "
          f"{get_status(risk_data['overall_score'])}"
      )

  st.subheader("Top Papers")
  for title in titles:
          st.write(title)

  st.subheader("Research Gaps")
  st.write(research_gap_output)
  st.subheader("Recommendation")
  st.write(recommendation)
