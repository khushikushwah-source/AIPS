# import json
# import streamlit as st
# import streamlit.components.v1 as components
# from firebase_config import users_ref

# st.set_page_config(page_title="AIPS — Hiring Process", page_icon="📋", layout="wide")

# # ------------- AUTH GUARD -------------
# if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
#     st.switch_page("pages/2_Login.py")

# user = st.session_state.get("user", {})
# email = user.get("email")
# domain = user.get("domain")
# company = user.get("company")

# if not email or not domain or not company:
#     st.warning("Please complete your domain and company selection first.")
#     st.switch_page("pages/4_Dashboard.py")

# # ------------- STYLES (NO SCROLL + PAGE LOOK) -------------
# st.markdown(
#     """
#     <style>
#     #MainMenu, header, footer {visibility:hidden;}
#     section[data-testid="stSidebar"] {display:none !important;}

#     html, body, [data-testid="stAppViewContainer"], .main {
#         height: 100vh !important;
#         overflow: hidden !important;
#         background: #020617;
#     }

#     .block-container {
#         padding-top: 0.5rem !important;
#     }

#     .hp-title-box {
#     margin: 40px auto 20px auto;
#     width: 80%;
#     padding: 26px;
#     border-radius: 20px;
#     background: rgba(10, 20, 35, 0.65);
#     border: 1px solid rgba(148,163,184,0.35);
#     box-shadow: 0 20px 60px rgba(2, 6, 23, 0.65);
#     text-align: center;
# }

# .hp-title-box .title-main {
#     font-size: 26px;
#     font-weight: 800;
#     color: #e2e8f0;
#     margin-bottom: 6px;
# }

# .hp-title-box .title-sub {
#     font-size: 15px;
#     color: #94a3b8;
# }

#     .hp-header {
#         width: 100%;
#         padding: 8px 16px 0 16px;
#         box-sizing: border-box;
#     }

#     .hp-back button {
#         border-radius: 999px;
#         padding: 6px 16px;
#         border: 1px solid rgba(226,232,240,0.7);
#         background: #064e3b;
#         color: #ecfeff;
#         font-weight: 600;
#     }

#     .hp-prof button {
#         width: 40px;
#         height: 40px;
#         border-radius: 999px;
#         background: #dc2626;
#         color: white;
#         border: none;
#         font-weight: 700;
#         font-size: 18px;
#         box-shadow: 0 8px 24px rgba(15,23,42,0.7);
#     }

#     .hp-main-card {
#         max-width: 980px;
#         margin: 80px auto 0 auto;
#         padding: 26px 26px 80px 26px;
#         border-radius: 18px;
#         background: rgba(15,23,42,0.97);
#         border: 1px solid rgba(148,163,184,0.6);
#         box-shadow: 0 24px 60px rgba(15,23,42,0.8);
#     }

#     .hp-main-card h2 {
#         margin-top: 0;
#         margin-bottom: 4px;
#     }

#     .hp-sub {
#         color: #a5b4fc;
#         font-size: 14px;
#         margin-bottom: 14px;
#     }

#     /* bottom-right Next */
#     .hp-next-fixed{
#         position: fixed !important;
#         right: 24px !important;
#         bottom: 24px !important;
#         z-index: 2000 !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ------------- HIRING PROCESS DATA -------------
# # Stage structure:
# # {
# #   "title": "...",
# #   "time": "...",
# #   "details": [ "...", ... ],
# #   "sections": [
# #       {
# #           "name": "...",
# #           "questions": "10",
# #           "time": "15 minutes",
# #           "topics": [
# #               {"topic": "Percentages", "questions": "1–2"},
# #               ...
# #           ]
# #       }, ...
# #   ]
# # }

# HIRING_DATA = {
#     "TCS": {
#         "Software Developer": [
#             {
#                 "title": "Online Aptitude Test",
#                 "time": "45 minutes",
#                 "details": [
#                     "Objective test with sections on Quantitative Aptitude, Logical Reasoning and Verbal Ability.",
#                 ],
#                 "sections": [
#                     {
#                         "name": "Quantitative Aptitude",
#                         "questions": "10",
#                         "time": "15 minutes (approx.)",
#                         "topics": [
#                             {"topic": "Percentages", "questions": "1–2"},
#                             {"topic": "Profit & Loss", "questions": "1–2"},
#                             {"topic": "Ratios & Proportion", "questions": "1–2"},
#                             {"topic": "Time & Work / Time & Distance", "questions": "2–3"},
#                         ],
#                     },
#                     {
#                         "name": "Logical Reasoning",
#                         "questions": "7",
#                         "time": "12–15 minutes (approx.)",
#                         "topics": [
#                             {"topic": "Series & Patterns", "questions": "2–3"},
#                             {"topic": "Puzzles / Arrangements", "questions": "2"},
#                             {"topic": "Data Sufficiency / Coding-Decoding", "questions": "2–3"},
#                         ],
#                     },
#                     {
#                         "name": "Verbal Ability",
#                         "questions": "8",
#                         "time": "15–18 minutes (approx.)",
#                         "topics": [
#                             {"topic": "Reading Comprehension", "questions": "3–4"},
#                             {"topic": "Error Spotting / Sentence Correction", "questions": "2–3"},
#                             {"topic": "Fill in the Blanks / Vocabulary", "questions": "1–2"},
#                         ],
#                     },
#                 ],
#             },
#             {
#                 "title": "Technical Assessment",
#                 "time": "60 minutes",
#                 "details": [
#                     "Data Structures & Algorithms coding questions",
#                     "OOPs concepts (Java/C++/Python)",
#                     "Basic DBMS & OS theory",
#                 ],
#             },
#             {
#                 "title": "Technical Interview Round(s)",
#                 "time": "30–45 minutes each",
#                 "details": [
#                     "Project discussion and core subject questions",
#                     "DSA problem solving discussion",
#                 ],
#             },
#             {
#                 "title": "HR Interview",
#                 "time": "20–30 minutes",
#                 "details": [
#                     "HR + Behavioural questions",
#                     "Salary, Location, Joining discussion",
#                 ],
#             },
#         ],
#         "Software Tester": [
#             {
#                 "title": "Online Aptitude + Logical Test",
#                 "time": "40 minutes",
#                 "details": [
#                     "Quant + Reasoning combined — 20–25 questions",
#                     "Basic English grammar & comprehension",
#                 ],
#             },
#             {
#                 "title": "QA / Testing Fundamentals Round",
#                 "time": "45 minutes",
#                 "details": [
#                     "Manual testing concepts (STLC, SDLC, test cases)",
#                     "Basic automation awareness (Selenium, tools – optional)",
#                 ],
#             },
#             {
#                 "title": "Technical + HR Interview",
#                 "time": "45–60 minutes",
#                 "details": [
#                     "Scenario based testing questions",
#                     "Behavioural & HR questions",
#                 ],
#             },
#         ],
#     },
#     "Infosys": {
#         "Software Developer": [
#             {
#                 "title": "Infosys Online Test",
#                 "time": "100 minutes",
#                 "details": [
#                     "Arithmetic Reasoning – 10 questions",
#                     "Analytical & Logical – 15 questions",
#                     "Verbal Ability – 20 questions",
#                 ],
#             },
#             {
#                 "title": "Coding + Pseudo Code Round",
#                 "time": "60 minutes",
#                 "details": [
#                     "2–3 coding problems (medium difficulty)",
#                     "Pseudo code and debugging questions",
#                 ],
#             },
#             {
#                 "title": "Technical Interview",
#                 "time": "30–45 minutes",
#                 "details": [
#                     "Languages (C/Java/Python) + DSA",
#                     "Database, OS, OOPs, project discussion",
#                 ],
#             },
#             {
#                 "title": "HR Interview",
#                 "time": "20–30 minutes",
#                 "details": [
#                     "Motivation, strengths, communication check",
#                 ],
#             },
#         ]
#     },
#     "Wipro": {
#         "Software Developer": [
#             {
#                 "title": "Online Aptitude & Verbal Test",
#                 "time": "48–60 minutes",
#                 "details": [
#                     "Quantitative Aptitude – 10–12 questions",
#                     "Logical Reasoning – 8–10 questions",
#                     "Verbal Ability – 15–20 questions",
#                 ],
#             },
#             {
#                 "title": "Coding + Essay Round",
#                 "time": "45–60 minutes",
#                 "details": [
#                     "1–2 coding problems (C/Java/Python)",
#                     "Short written communication / essay",
#                 ],
#             },
#             {
#                 "title": "Technical + HR Interview",
#                 "time": "45–60 minutes",
#                 "details": [
#                     "Technical concepts, projects, resume discussion",
#                     "HR questions and offer discussion",
#                 ],
#             },
#         ]
#     },
# }


# def generate_generic_process(company_name: str, domain_name: str):
#     """Fallback generic process for unknown company/domain."""
#     d = domain_name.lower()
#     dev_extra = []
#     if "data" in d:
#         dev_extra = [
#             "SQL queries, basic statistics (mean, median, variance)",
#             "Data interpretation questions on charts / tables",
#         ]
#     elif "tester" in d:
#         dev_extra = [
#             "Basic testing concepts (test case, bug life cycle)",
#             "Scenario-based questions on finding defects",
#         ]
#     else:
#         dev_extra = [
#             "Basic coding questions",
#             "Conceptual questions from CS fundamentals",
#         ]

#     generic = [
#         {
#             "title": "Online Aptitude Test",
#             "time": "40–45 minutes",
#             "details": [
#                 "Objective sections on Quantitative Aptitude, Logical Reasoning and English.",
#             ],
#             "sections": [
#                 {
#                     "name": "Quantitative Aptitude",
#                     "questions": "10",
#                     "time": "15 minutes (approx.)",
#                     "topics": [
#                         {"topic": "Percentages / Ratios", "questions": "2–3"},
#                         {"topic": "Profit & Loss / Simple Interest", "questions": "2–3"},
#                         {"topic": "Time, Speed, Work", "questions": "2–3"},
#                     ],
#                 },
#                 {
#                     "name": "Logical Reasoning",
#                     "questions": "7–8",
#                     "time": "10–12 minutes (approx.)",
#                     "topics": [
#                         {"topic": "Series / Patterns", "questions": "2–3"},
#                         {"topic": "Puzzles / Seating", "questions": "2–3"},
#                         {"topic": "Data Sufficiency", "questions": "1–2"},
#                     ],
#                 },
#                 {
#                     "name": "Verbal Ability",
#                     "questions": "8–10",
#                     "time": "15–18 minutes (approx.)",
#                     "topics": [
#                         {"topic": "Reading Comprehension", "questions": "3–4"},
#                         {"topic": "Grammar / Error Spotting", "questions": "2–3"},
#                         {"topic": "Vocabulary / Fill in the blanks", "questions": "1–2"},
#                     ],
#                 },
#             ],
#         },
#         {
#             "title": "Technical Assessment",
#             "time": "45–60 minutes",
#             "details": dev_extra,
#         },
#         {
#             "title": "Technical Interview",
#             "time": "30–45 minutes",
#             "details": [
#                 "Discussion on projects and internships",
#                 "Questions on core subjects & problem solving",
#             ],
#         },
#         {
#             "title": "HR Interview",
#             "time": "20–30 minutes",
#             "details": [
#                 "Behavioural and cultural fit questions",
#                 "Discussion on role, location, and joining date",
#             ],
#         },
#     ]
#     return generic


# def get_hiring_process(company_name: str, domain_name: str):
#     c = HIRING_DATA.get(company_name)
#     if c:
#         d = c.get(domain_name)
#         if d:
#             return d, None
#         msg = (
#             f"We don't have a domain-specific chart for **{domain_name}** at **{company_name}**. "
#             "Showing a predicted generic hiring process instead."
#         )
#         return generate_generic_process(company_name, domain_name), msg
#     msg = (
#         f"**Note:** We don't have official data for **{company_name}**. "
#         "This company may not exist in our database, so we are showing a predicted hiring process for practice."
#     )
#     return generate_generic_process(company_name, domain_name), msg


# stages, info_msg = get_hiring_process(company, domain)

# # ------------- HEADER (Back + Profile) -------------
# st.markdown('<div class="hp-header">', unsafe_allow_html=True)
# h_left, h_spacer, h_right = st.columns([1, 6, 1])

# with h_left:
#     with st.container():
#         back_clicked = st.button("← Back", key="hp_back")
#     st.markdown('<div class="hp-back"></div>', unsafe_allow_html=True)

# with h_right:
#     avatar_label = (user.get("name") or "U")[0].upper()
#     with st.popover(avatar_label):
#         st.write(f"**{user.get('name','User')}**")
#         st.write(user.get("email", ""))
#         st.markdown(f"""
#         <div class="hp-title-box">
#         <div class="title-main">{company} — {domain} Hiring Process</div>
#         <div class="title-sub">Based on your selection, here is the typical selection flow.</div>
#         </div>
#         """, unsafe_allow_html=True)
#         if st.button("My Profile 👤"):
#             st.switch_page("pages/5_My_Profile.py")
#         if st.button("Logout ⏻"):
#             st.session_state.clear()
#             st.switch_page("pages/0_Welcome.py")
#     st.markdown('<div class="hp-prof"></div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# if back_clicked:
#     st.switch_page("pages/4_Dashboard.py")

# # ------------- MAIN CARD (TITLE + DRAWFLOW + DETAILS) -------------
# st.markdown(f"""
# <div class="hp-title-box">
#     {company} — {domain} Hiring Process
# </div>
# """, unsafe_allow_html=True)

# if info_msg:
#     st.info(info_msg)

# # -------- DRAWFLOW DIAGRAM (top flowchart) --------
# js_stages = [
#     {
#         "id": idx + 1,
#         "title": stage.get("title", f"Stage {idx+1}"),
#         "time": stage.get("time", ""),
#     }
#     for idx, stage in enumerate(stages)
# ]

# drawflow_html = """
# <!DOCTYPE html>
# <html>
#   <head>
#     <link rel="stylesheet" href="https://unpkg.com/drawflow@0.0.46/dist/drawflow.min.css">
#     <style>
#       body {
#         margin: 0;
#         background: transparent;
#         font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
#       }
#       #drawflow-wrapper {
#         width: 100%;
#         height: 220px;
#         background: transparent;
#       }
#       #drawflow {
#         width: 100%;
#         height: 100%;
#         background: linear-gradient(135deg,#020617,#020617);
#       }
#       .drawflow .node {
#         width: 190px;
#         background: #020617;
#         border-radius: 14px;
#         border: 1px solid rgba(148,163,184,0.9);
#         color: #e5e7eb;
#         box-shadow: 0 18px 40px rgba(15,23,42,0.9);
#         text-align: center;
#         padding: 8px 6px;
#       }
#       .node-title {
#         font-size: 13px;
#         font-weight: 600;
#         margin-bottom: 3px;
#       }
#       .node-time {
#         font-size: 11px;
#         color: #a5b4fc;
#       }
#       .drawflow .connection .main-path {
#         stroke: #a5b4fc;
#         stroke-width: 2;
#         stroke-dasharray: 6 4;
#         animation: dash 1.5s linear infinite;
#       }
#       @keyframes dash {
#         to {
#           stroke-dashoffset: -20;
#         }
#       }
#       .drawflow .input, .drawflow .output {
#         background: #22c55e;
#         border: none;
#         width: 8px;
#         height: 8px;
#       }
#     </style>
#   </head>
#   <body>
#     <div id="drawflow-wrapper">
#       <div id="drawflow"></div>
#     </div>

#     <script src="https://unpkg.com/drawflow@0.0.46/dist/drawflow.min.js"></script>
#     <script>
#       const stages = STAGES_JSON;

#       const editor = new Drawflow(document.getElementById('drawflow'));
#       editor.reroute = true;
#       editor.curvature = 0.5;
#       editor.zoom_max = 1.2;
#       editor.zoom_min = 0.5;
#       editor.start();

#       const widthStep = 230;
#       const baseX = 60;
#       const baseY = 80;

#       stages.forEach((s, idx) => {
#         const html = `
#           <div class="node-title">${idx + 1}️⃣ ${s.title}</div>
#           <div class="node-time">${s.time ? "⏱ " + s.time : ""}</div>
#         `;
#         const data = { title: s.title, time: s.time };
#         const nodeId = editor.addNode(
#           "stage" + s.id,
#           1,
#           1,
#           baseX + idx * widthStep,
#           baseY,
#           "stage-node",
#           data,
#           html
#         );
#         s._drawflow_id = nodeId;
#       });

#       for (let i = 0; i < stages.length - 1; i++) {
#         const from = stages[i]._drawflow_id;
#         const to = stages[i+1]._drawflow_id;
#         editor.addConnection(from, to, "output_1", "input_1");
#       }

#       editor.zoom_out();
#     </script>
#   </body>
# </html>
# """

# drawflow_html = drawflow_html.replace("STAGES_JSON", json.dumps(js_stages))
# components.html(drawflow_html, height=230, scrolling=False)

# st.markdown("---")

# # -------- DETAIL EXPANDERS (Stage → Sections → Topics) --------
# for idx, stage in enumerate(stages, start=1):
#     title = stage.get("title", f"Stage {idx}")
#     time_info = stage.get("time", "")
#     header = f"{idx}️⃣  {title}"
#     if time_info:
#         header += f"  ·  ⏱ {time_info}"

#     with st.expander(header, expanded=(idx == 1)):
#         sections = stage.get("sections")
#         if sections:
#             for sec in sections:
#                 s_name = sec.get("name", "Section")
#                 s_q = sec.get("questions", "")
#                 s_time = sec.get("time", "")
#                 sec_header = s_name
#                 bits = []
#                 if s_q:
#                     bits.append(f"{s_q} Q")
#                 if s_time:
#                     bits.append(s_time)
#                 if bits:
#                     sec_header += "  ·  " + " · ".join(bits)

#                 with st.expander(sec_header):
#                     for t in sec.get("topics", []):
#                         t_name = t.get("topic", "Topic")
#                         t_q = t.get("questions", "")
#                         if t_q:
#                             st.markdown(f"- **{t_name}** — {t_q} questions")
#                         else:
#                             st.markdown(f"- **{t_name}**")

#         details = stage.get("details", [])
#         if details:
#             if sections:
#                 st.markdown("---")
#                 st.markdown("**Overview:**")
#             for line in details:
#                 st.markdown(f"- {line}")

# st.markdown("</div>", unsafe_allow_html=True)

# # ------------- NEXT BUTTON (to Test Session) -------------
# next_clicked = st.button("Next ➜", key="hp_next")

# st.markdown(
#     """
#     <script>
#     const btns = Array.from(window.parent.document.querySelectorAll("button"));
#     btns.forEach(b => {
#         if (b.innerText.trim() === "Next ➜") {
#             b.classList.add("hp-next-fixed");
#         }
#     });
#     </script>
#     """,
#     unsafe_allow_html=True,
# )

# if next_clicked:
#     try:
#         st.switch_page("pages/7_Test_Session.py")  # A: 7_Test_Session.py
#     except Exception:
#         st.warning("Test session page is not created yet (pages/7_Test_Session.py).")


import streamlit as st
import streamlit.components.v1 as components

with open("E:/hiring-flow/build/index.html", "r", encoding="utf-8") as file:
    page = file.read()

components.html(page, height=700, scrolling=False)
