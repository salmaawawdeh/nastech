# -*- coding: utf-8 -*-
from datetime import date, datetime
import html
import pandas as pd
import streamlit as st
from supabase import create_client

# =====================================================
# 1. إعداد الصفحة والتصميم
# =====================================================
st.set_page_config(
    page_title="منصة الفعاليات والورشات الجامعية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(15,23,42,.90), rgba(15,23,42,.92)),
        url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #f8fafc;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}
.main-header {
    text-align: center;
    padding: 25px 15px;
    margin-bottom: 28px;
    background: rgba(255,255,255,.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,.15);
    border-bottom: 3px solid #818cf8;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,.25);
}
.main-header h1 {
    color: #fff;
    font-size: clamp(24px, 3vw, 38px);
    font-weight: 800;
}
.main-header p {
    color: #cbd5e1;
    font-size: 17px;
}
.role-card {
    background: rgba(255,255,255,.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 18px;
    padding: 28px 20px;
    text-align: center;
    min-height: 190px;
    box-shadow: 0 8px 32px rgba(0,0,0,.25);
    margin-bottom: 15px;
    transition: .3s ease;
}
.role-card:hover {
    transform: translateY(-5px);
    border-color: #818cf8;
}
.role-icon {
    font-size: 48px;
    margin-bottom: 12px;
}
.event-card {
    background: rgba(255,255,255,.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,.17);
    border-radius: 16px;
    padding: 22px;
    margin: 15px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,.28);
    overflow-wrap: anywhere;
}
.event-card h3 { color: #a5b4fc; }
.event-card p {
    color: #e2e8f0;
    line-height: 1.8;
}
h1, h2, h3, h4 { color: #f8fafc; }
p, label { color: #e2e8f0; }

button[data-baseweb="tab"] {
    background: transparent !important;
    color: #cbd5e1 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #a5b4fc !important;
    border-bottom: 3px solid #818cf8 !important;
}
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg,#6366f1,#4f46e5) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 18px !important;
    width: 100%;
    transition: .25s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg,#818cf8,#6366f1) !important;
    box-shadow: 0 4px 18px rgba(99,102,241,.35);
}
.stTextInput input, .stTextArea textarea {
    background-color: rgba(15,23,42,.8) !important;
    color: white !important;
    border: 1px solid #475569 !important;
    border-radius: 9px !important;
}
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    border-color: #475569 !important;
    color: white !important;
}
section[data-testid="stSidebar"] {
    background: rgba(15,23,42,.97);
}
div[data-testid="stDataFrame"] {
    background: rgba(30,41,59,.9) !important;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px;
    padding: 8px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(255,255,255,.16) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,.035);
}
div[data-testid="stAlert"] { border-radius: 10px; }
hr { border-color: rgba(255,255,255,.15) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 البوابة الإلكترونية للفعاليات والورشات الجامعية</h1>
    <p>منصة موحدة لاستكشاف الفعاليات والتسجيل وإدارة الحجوزات ومتابعة الحضور</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 2. الاتصال بقاعدة البيانات
# =====================================================
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()

    if not url.startswith("https://") or not url.endswith(".supabase.co"):
        raise ValueError("تحقق من رابط مشروع Supabase.")

    return create_client(url, key)


try:
    supabase = get_supabase()
except Exception as e:
    st.error("تعذر الاتصال بـ Supabase.")
    st.code(f"{type(e).__name__}: {e}")
    st.info(
        "أنشئ الملف .streamlit/secrets.toml وضلع فيه "
        "SUPABASE_URL وSUPABASE_KEY."
    )
    st.stop()


def db_error(message, error):
    st.error(message)
    st.code(f"{type(error).__name__}: {error}")


def read_table(table, columns="*"):
    return supabase.table(table).select(columns).execute()


def safe_int(value, default=0):
    try:
        if pd.isna(value):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def clean(value):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def display_date(value):
    return clean(value) or "غير محدد"


# =====================================================
# 3. جلب بيانات الجداول
# =====================================================
try:
    users_df = pd.DataFrame(
        read_table("users", "user_id, name, email, role, major").data or []
    )
    events_df = pd.DataFrame(
        read_table(
            "events",
            "event_id, title, description, category, event_date, "
            "venue_id, organizer_id, status, rejection_reason"
        ).data or []
    )
    venues_df = pd.DataFrame(
        read_table(
            "venues",
            "venue_id, venue_name, university_name, max_capacity"
        ).data or []
    )
    registrations_df = pd.DataFrame(
        read_table(
            "registrations",
            "registration_id, student_id, event_id, attendance_status"
        ).data or []
    )
except Exception as e:
    db_error("تعذر جلب بيانات قاعدة البيانات.", e)
    st.stop()


columns_map = {
    "users": ["user_id", "name", "email", "role", "major"],
    "events": [
        "event_id", "title", "description", "category", "event_date",
        "venue_id", "organizer_id", "status", "rejection_reason"
    ],
    "venues": [
        "venue_id", "venue_name", "university_name", "max_capacity"
    ],
    "registrations": [
        "registration_id", "student_id", "event_id", "attendance_status"
    ],
}

for name, cols in columns_map.items():
    df = {
        "users": users_df,
        "events": events_df,
        "venues": venues_df,
        "registrations": registrations_df,
    }[name]

    for col in cols:
        if col not in df.columns:
            df[col] = pd.Series(dtype="object")


for df, cols in [
    (users_df, ["user_id"]),
    (events_df, ["event_id", "venue_id", "organizer_id"]),
    (venues_df, ["venue_id", "max_capacity"]),
    (registrations_df, ["registration_id", "student_id", "event_id"]),
]:
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")


def event_venue(event):
    venue_id = event.get("venue_id")
    if pd.isna(venue_id):
        return {}
    rows = venues_df[venues_df["venue_id"] == venue_id]
    return rows.iloc[0].to_dict() if not rows.empty else {}


def event_registrations(event_id):
    return registrations_df[
        registrations_df["event_id"] == safe_int(event_id, -1)
    ].copy()


def registration_count(event_id):
    return len(event_registrations(event_id))


def capacity_for_event(event):
    return max(0, safe_int(event_venue(event).get("max_capacity")))


def venue_label(venue):
    return (
        f"{clean(venue.get('venue_name'))} - "
        f"{clean(venue.get('university_name'))} "
        f"(السعة: {safe_int(venue.get('max_capacity'))})"
    )


def get_user_name(user_id):
    rows = users_df[
        users_df["user_id"] == safe_int(user_id, -1)
    ]
    if rows.empty:
        return f"مستخدم #{user_id}"
    return clean(rows.iloc[0].get("name")) or f"مستخدم #{user_id}"


# =====================================================
# 4. اختيار الدور والحساب
# =====================================================
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

if "current_user_id" not in st.session_state:
    st.session_state["current_user_id"] = None

if "company_portal" not in st.session_state:
    st.session_state["company_portal"] = False

if "company_request" not in st.session_state:
    st.session_state["company_request"] = None


role_labels = {
    "student": "👨‍🎓 طالب",
    "organizer": "📋 منظم فعاليات",
    "admin": "🏛️ إدارة الجامعة",
}

# =====================================================
# 4-A. بوابة الشركات والمنظمات
# لا تستخدم قاعدة البيانات
# =====================================================
if st.session_state["company_portal"]:
    st.markdown("## 🏢 بوابة الشركات والمنظمات")
    st.write(
        "أدخل بيانات الشركة والمكان المقترح لإقامة "
        "الورشات والفعاليات الجامعية."
    )

    with st.form("company_request_form", clear_on_submit=False):
        company_name = st.text_input("🏢 اسم الشركة أو المنظمة")
        company_location = st.text_input("📍 موقع الشركة")
        event_location = st.text_input(
            "🏛️ المكان المقترح لإقامة الورشة أو الفعالية"
        )

        submit_company = st.form_submit_button("عرض بيانات الشركة")

    if submit_company:
        if not all([
            company_name.strip(),
            company_location.strip(),
            event_location.strip(),
        ]):
            st.warning("يرجى تعبئة جميع الحقول.")
        else:
            st.session_state["company_request"] = {
                "company_name": company_name.strip(),
                "company_location": company_location.strip(),
                "event_location": event_location.strip(),
            }

    request = st.session_state["company_request"]

    if request:
        st.success("تم إدخال بيانات الشركة بنجاح.")

        st.markdown(
            f"**اسم الشركة:** "
            f"{html.escape(request['company_name'])}"
        )
        st.markdown(
            f"**موقع الشركة:** "
            f"{html.escape(request['company_location'])}"
        )
        st.markdown(
            f"**مكان إقامة الفعالية:** "
            f"{html.escape(request['event_location'])}"
        )

        st.caption(
            "هذه بيانات تجريبية محفوظة خلال الجلسة الحالية فقط، "
            "ولا يتم إرسالها إلى قاعدة البيانات."
        )

    if st.button("⬅️ العودة إلى الصفحة الرئيسية"):
        st.session_state["company_portal"] = False
        st.session_state["company_request"] = None
        st.rerun()

    st.stop()


if st.session_state["user_role"] is None:
    st.markdown("## 🏛️ اختر بوابتك للدخول")
    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">👨‍🎓</div>
            <h3>بوابة الطلاب</h3>
            <p>استكشاف الفعاليات والتسجيل ومتابعة الحضور.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("الدخول كطالب", key="choose_student"):
            st.session_state["user_role"] = "student"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">📋</div>
            <h3>منظم الفعاليات</h3>
            <p>إنشاء الفعاليات ومتابعة الطلبات وإدارة الحضور.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("الدخول كمنظم", key="choose_organizer"):
            st.session_state["user_role"] = "organizer"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🏛️</div>
            <h3>إدارة الجامعة</h3>
            <p>مراجعة طلبات الفعاليات وقبولها أو رفضها.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("الدخول كإدارة", key="choose_admin"):
            st.session_state["user_role"] = "admin"
            st.rerun()

    # البطاقة الإضافية للشركات والمنظمات
    st.write("")

    company_cols = st.columns([1, 1, 1])

    with company_cols[1]:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🏢</div>
            <h3>الشركات والمنظمات</h3>
            <p>إدخال بيانات الشركات واقتراح أماكن الورشات والفعاليات.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "الدخول للشركات والمنظمات",
            key="choose_company"
        ):
            st.session_state["company_portal"] = True
            st.rerun()

    st.warning(
        "اختيار الدور للتجربة فقط وليس تسجيل دخول آمناً. "
        "استخدم نظام مصادقة وصلاحيات قبل نشر التطبيق."
    )
    st.stop()


current_role = st.session_state["user_role"]

role_users = users_df[
    users_df["role"].astype(str).str.lower() == current_role
].copy()


# =====================================================
# إضافة طالب جديد
# =====================================================
if current_role == "student":
    with st.expander("➕ تسجيل طالب جديد", expanded=role_users.empty):
        with st.form("add_student_form", clear_on_submit=True):
            new_name = st.text_input("اسم الطالب")
            new_email = st.text_input("البريد الإلكتروني")
            new_major = st.text_input("التخصص")
            add_student = st.form_submit_button("حفظ الطالب")

        if add_student:
            if not all([
                new_name.strip(),
                new_email.strip(),
                new_major.strip()
            ]):
                st.warning("يرجى تعبئة الاسم والبريد والتخصص.")

            elif "@" not in new_email or "." not in new_email.split("@")[-1]:
                st.warning("يرجى إدخال بريد إلكتروني صحيح.")

            elif users_df["email"].fillna("").astype(str).str.lower().eq(
                new_email.strip().lower()
            ).any():
                st.warning("هذا البريد الإلكتروني مسجل مسبقاً.")

            else:
                try:
                    result = supabase.table("users").insert({
                        "name": new_name.strip(),
                        "email": new_email.strip(),
                        "major": new_major.strip(),
                        "role": "student",
                    }).execute()

                    if result.data:
                        st.session_state["current_user_id"] = (
                            result.data[0].get("user_id")
                        )
                        st.success("تم تسجيل الطالب بنجاح.")
                        st.rerun()
                    else:
                        st.warning(
                            "لم ترجع قاعدة البيانات بيانات الطالب."
                        )

                except Exception as e:
                    db_error("تعذرت إضافة الطالب.", e)


if role_users.empty:
    st.warning(
        f"لا يوجد حساب بدور {role_labels[current_role]} "
        "في جدول users."
    )
    st.info("أضف حساباً بهذا الدور في قاعدة البيانات أولاً.")

    if st.button("العودة لاختيار الدور"):
        st.session_state["user_role"] = None
        st.session_state["current_user_id"] = None
        st.rerun()

    st.stop()


saved_id = st.session_state.get("current_user_id")

saved_matches = (
    role_users[role_users["user_id"] == safe_int(saved_id, -1)]
    if saved_id is not None
    else pd.DataFrame()
)

if not saved_matches.empty:
    current_user = saved_matches.iloc[0].to_dict()

elif len(role_users) == 1:
    current_user = role_users.iloc[0].to_dict()

else:
    role_users = role_users.reset_index(drop=True)

    chosen_idx = st.selectbox(
        "اختر الحساب:",
        list(range(len(role_users))),
        format_func=lambda i: (
            f"{clean(role_users.iloc[i].get('name'))} — "
            f"{clean(role_users.iloc[i].get('email'))}"
        ),
    )

    current_user = role_users.iloc[chosen_idx].to_dict()
    st.session_state["current_user_id"] = safe_int(
        current_user["user_id"]
    )


current_user_id = safe_int(current_user.get("user_id"), -1)


# =====================================================
# خانة اسم المنظّم وتحديثه
# =====================================================
if current_role == "organizer":
    with st.expander("👤 بيانات المنظّم", expanded=True):
        with st.form("organizer_name_form"):
            organizer_name = st.text_input(
                "اسم المنظّم",
                value=clean(current_user.get("name")),
            )

            save_organizer_name = st.form_submit_button(
                "حفظ اسم المنظّم"
            )

        if save_organizer_name:
            if not organizer_name.strip():
                st.warning("يرجى إدخال اسم المنظّم.")
            else:
                try:
                    supabase.table("users").update({
                        "name": organizer_name.strip()
                    }).eq(
                        "user_id", current_user_id
                    ).eq(
                        "role", "organizer"
                    ).execute()

                    st.success("تم حفظ اسم المنظّم بنجاح.")
                    st.rerun()

                except Exception as e:
                    db_error("تعذر تحديث اسم المنظّم.", e)


top1, top2 = st.columns([4, 1])

with top1:
    st.write(
        f"**الحساب الحالي:** {clean(current_user.get('name'))} "
        f"| **الدور:** {role_labels[current_role]}"
    )

with top2:
    if st.button("🔄 تغيير الدور"):
        st.session_state["user_role"] = None
        st.session_state["current_user_id"] = None
        st.rerun()


st.divider()


# =====================================================
# 5. واجهة الطالب
# =====================================================
if current_role == "student":

    with st.sidebar:
        st.subheader("👤 ملف الطالب")

        updated_major = st.text_input(
            "التخصص الأكاديمي",
            value=clean(current_user.get("major")),
            key=f"major_{current_user_id}",
        )

        if st.button("حفظ التخصص"):
            try:
                supabase.table("users").update({
                    "major": updated_major.strip()
                }).eq("user_id", current_user_id).execute()

                st.success("تم تحديث التخصص.")
                st.rerun()

            except Exception as e:
                db_error("تعذر تحديث التخصص.", e)


    tab1, tab2, tab3 = st.tabs([
        "📌 الفعاليات المتاحة",
        "🎒 فعالياتي",
        "✨ توصيات مناسبة لي",
    ])

    approved_events = events_df[
        events_df["status"].astype(str).str.lower() == "approved"
    ].copy()


    # -------------------------------------------------
    # الفعاليات المتاحة
    # -------------------------------------------------
    with tab1:
        st.subheader("استكشاف الفعاليات والورشات")

        search_col, category_col = st.columns(2)

        search_text = search_col.text_input("🔍 البحث باسم الفعالية")

        categories = ["الكل"] + sorted({
            clean(x)
            for x in approved_events["category"].dropna()
            if clean(x)
        })

        selected_category = category_col.selectbox(
            "التصنيف", categories
        )

        shown_events = approved_events.copy()

        if search_text.strip():
            shown_events = shown_events[
                shown_events["title"].fillna("").astype(str).str.contains(
                    search_text.strip(),
                    case=False,
                    na=False
                )
            ]

        if selected_category != "الكل":
            shown_events = shown_events[
                shown_events["category"].astype(str)
                == selected_category
            ]

        if shown_events.empty:
            st.info("لا توجد فعاليات مطابقة حالياً.")

        else:
            for _, ev in shown_events.iterrows():
                event_id = safe_int(ev["event_id"])
                venue = event_venue(ev)
                count = registration_count(event_id)
                capacity = capacity_for_event(ev)
                seats = capacity - count

                st.markdown(f"""
                <div class="event-card">
                    <h3>📌 {html.escape(clean(ev.get('title')))}</h3>
                    <p><b>المكان:</b>
                    {html.escape(clean(venue.get('venue_name')))}
                    — {html.escape(clean(venue.get('university_name')))}</p>
                    <p><b>التاريخ:</b>
                    {html.escape(display_date(ev.get('event_date')))}</p>
                    <p><b>التصنيف:</b>
                    {html.escape(clean(ev.get('category')))}</p>
                    <p><b>الوصف:</b>
                    {html.escape(clean(ev.get('description')))}</p>
                    <p><b>المسجلون:</b> {count} |
                    <b>المقاعد المتبقية:</b>
                    {seats if capacity else 'السعة غير محددة'}</p>
                </div>
                """, unsafe_allow_html=True)

                my_reg = registrations_df[
                    (registrations_df["student_id"] == current_user_id)
                    & (registrations_df["event_id"] == event_id)
                ]

                if not my_reg.empty:
                    st.success("✅ أنت مسجل في هذه الفعالية.")

                elif capacity > 0 and seats <= 0:
                    st.error("❌ اكتملت المقاعد.")

                elif st.button(
                    "التسجيل في الفعالية",
                    key=f"register_{event_id}"
                ):
                    try:
                        supabase.table("registrations").insert({
                            "student_id": current_user_id,
                            "event_id": event_id,
                            "attendance_status": "absent",
                        }).execute()

                        st.success("تم تسجيلك بنجاح.")
                        st.rerun()

                    except Exception as e:
                        db_error(
                            "تعذر التسجيل. ربما أنت مسجل مسبقاً.",
                            e
                        )


    # -------------------------------------------------
    # فعالياتي
    # -------------------------------------------------
    with tab2:
        st.subheader("الفعاليات التي سجلت فيها")

        my_regs = registrations_df[
            registrations_df["student_id"] == current_user_id
        ].copy()

        my_rows = []

        for _, reg in my_regs.iterrows():
            rows = events_df[
                events_df["event_id"]
                == safe_int(reg.get("event_id"), -1)
            ]

            if rows.empty:
                continue

            ev = rows.iloc[0]
            venue = event_venue(ev)

            my_rows.append({
                "الفعالية": clean(ev.get("title")),
                "التاريخ": display_date(ev.get("event_date")),
                "التصنيف": clean(ev.get("category")),
                "المكان": clean(venue.get("venue_name")),
                "حالة الفعالية": clean(ev.get("status")),
                "الحضور": (
                    "حاضر"
                    if clean(
                        reg.get("attendance_status")
                    ).lower() == "present"
                    else "غائب"
                ),
            })

        if my_rows:
            st.dataframe(
                pd.DataFrame(my_rows),
                use_container_width=True
            )
        else:
            st.info("لم تسجل في أي فعالية حتى الآن.")


    # -------------------------------------------------
    # التوصيات المحسنة
    # -------------------------------------------------
    with tab3:
        st.subheader("✨ توصيات حسب التخصص والتصنيف")

        major = clean(current_user.get("major")).strip().lower()

        registered_ids = set(
            my_regs["event_id"].dropna().astype(int).tolist()
        ) if not my_regs.empty else set()

        recommendations = []

        for _, ev in approved_events.iterrows():
            event_id = safe_int(ev.get("event_id"))

            if event_id in registered_ids:
                continue

            category = clean(ev.get("category"))
            description = clean(ev.get("description"))
            title = clean(ev.get("title"))

            searchable = f"{category} {description} {title}".lower()

            score = 50
            reasons = ["فعالية معتمدة"]

            if major and major in searchable:
                score += 30
                reasons.append("تطابق نصي مع التخصص")

            if category:
                score += 10
                reasons.append(f"التصنيف: {category}")

            recommendations.append({
                "event": ev,
                "score": min(score, 100),
                "reason": "؛ ".join(reasons),
            })

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        if not recommendations:
            if approved_events.empty:
                st.info(
                    "لا توجد فعاليات معتمدة حالياً. "
                    "ستظهر الفعاليات هنا عند اعتمادها من إدارة الجامعة."
                )

            else:
                st.info(
                    "لا توجد توصيات جديدة بناءً على تسجيلاتك الحالية. "
                    "إليك الفعاليات المعتمدة المتاحة للاطلاع عليها."
                )

                for _, ev in approved_events.iterrows():
                    event_id = safe_int(ev.get("event_id"))
                    venue = event_venue(ev)
                    count = registration_count(event_id)
                    capacity = capacity_for_event(ev)
                    seats = capacity - count

                    st.markdown(f"""
                    <div class="event-card">
                        <h3>📌 {html.escape(clean(ev.get('title')))}</h3>
                        <p>التصنيف:
                        {html.escape(clean(ev.get('category')))}</p>
                        <p>التاريخ:
                        {html.escape(display_date(ev.get('event_date')))}</p>
                        <p>المكان:
                        {html.escape(clean(venue.get('venue_name')))}</p>
                        <p>الوصف:
                        {html.escape(clean(ev.get('description')))}</p>
                        <p>المقاعد المتبقية:
                        {seats if capacity else 'السعة غير محددة'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    my_reg = registrations_df[
                        (registrations_df["student_id"] == current_user_id)
                        & (registrations_df["event_id"] == event_id)
                    ]

                    if not my_reg.empty:
                        st.success("✅ أنت مسجل في هذه الفعالية.")

                    elif capacity > 0 and seats <= 0:
                        st.error("❌ اكتملت المقاعد.")

                    elif st.button(
                        "التسجيل في الفعالية",
                        key=f"recommend_fallback_{event_id}"
                    ):
                        try:
                            supabase.table("registrations").insert({
                                "student_id": current_user_id,
                                "event_id": event_id,
                                "attendance_status": "absent",
                            }).execute()

                            st.success("تم التسجيل بنجاح.")
                            st.rerun()

                        except Exception as e:
                            db_error(
                                "تعذر التسجيل في الفعالية.",
                                e
                            )

        else:
            for item in recommendations[:10]:
                ev = item["event"]
                event_id = safe_int(ev.get("event_id"))

                st.markdown(f"""
                <div class="event-card">
                    <h3>✨ {html.escape(clean(ev.get('title')))}</h3>
                    <p>التصنيف:
                    {html.escape(clean(ev.get('category')))}</p>
                    <p>التاريخ:
                    {html.escape(display_date(ev.get('event_date')))}</p>
                    <p>درجة الملاءمة التقديرية:
                    {item['score']}%</p>
                </div>
                """, unsafe_allow_html=True)

                st.progress(item["score"] / 100)
                st.write(item["reason"])

                if st.button(
                    "التسجيل في الفعالية",
                    key=f"recommend_{event_id}"
                ):
                    try:
                        supabase.table("registrations").insert({
                            "student_id": current_user_id,
                            "event_id": event_id,
                            "attendance_status": "absent",
                        }).execute()

                        st.success("تم التسجيل بنجاح.")
                        st.rerun()

                    except Exception as e:
                        db_error(
                            "تعذر التسجيل في الفعالية.",
                            e
                        )


# =====================================================
# 6. واجهة المنظم
# =====================================================
elif current_role == "organizer":

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ إنشاء فعالية",
        "📬 طلباتي",
        "📋 المسجلون والحضور",
        "📊 الإحصائيات",
    ])

    # -------------------------------------------------
    # إنشاء فعالية
    # -------------------------------------------------
    with tab1:
        st.subheader("إنشاء فعالية جديدة")

        if venues_df.empty:
            st.warning(
                "لا توجد قاعات أو مدرجات في جدول venues."
            )

        else:
            venue_records = venues_df.to_dict("records")

            venue_ids = [
                safe_int(v.get("venue_id"))
                for v in venue_records
            ]

            venue_map = {
                safe_int(v.get("venue_id")): v
                for v in venue_records
            }

            with st.form("create_event_form"):
                title = st.text_input("عنوان الفعالية")
                description = st.text_area("الوصف")

                category = st.selectbox(
                    "التصنيف",
                    ["تقني", "فني", "رياضي", "ثقافي", "عام"]
                )

                event_date = st.date_input(
                    "تاريخ الفعالية",
                    min_value=date.today(),
                    value=date.today(),
                )

                event_time = st.time_input("وقت الفعالية")

                venue_id = st.selectbox(
                    "القاعة / المدرج",
                    venue_ids,
                    format_func=lambda v: venue_label(venue_map[v]),
                )

                submit_event = st.form_submit_button(
                    "إرسال للمراجعة"
                )

            if submit_event:
                if not title.strip():
                    st.warning("يرجى كتابة عنوان الفعالية.")

                else:
                    try:
                        full_datetime = datetime.combine(
                            event_date,
                            event_time
                        ).isoformat()

                        supabase.table("events").insert({
                            "title": title.strip(),
                            "description": description.strip(),
                            "category": category,
                            "event_date": full_datetime,
                            "venue_id": venue_id,
                            "organizer_id": current_user_id,
                            "status": "pending",
                        }).execute()

                        st.success(
                            "تم إرسال الفعالية بنجاح وهي بانتظار الاعتماد."
                        )
                        st.rerun()

                    except Exception as e:
                        db_error("تعذر إنشاء الفعالية.", e)