import streamlit as st
import pandas as pd
from groq import Groq

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI ERP Dashboard")

# ------------------ GROQ AI ------------------
client = Groq(api_key=st.secrets["GROQ_API"])


def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an ERP business analyst AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

# ------------------ USERS ------------------
USERS = {
    "kingston": {"password": "king@123", "role": "admin"},
    "joy": {"password": "joy@123", "role": "user"}
}

# ------------------ SESSION STATE INIT ------------------
defaults = {
    "logged_in": False,
    "user": None,
    "role": None,
    "stock_df": pd.DataFrame(),
    "stock": {},
    "sold": {},
    "orders": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------ LOGIN ------------------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = user["role"]
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# ------------------ LOAD & GROUP CSV (ONCE) ------------------
if st.session_state.stock_df.empty:
    df = pd.read_csv("erp_sales_data.csv")

    df_grouped = df.groupby("product", as_index=False).agg({
        "quantity": "sum",
        "price": "first"
    })

    category_map = {
        "Mouse": "Accessories",
        "Keyboard": "Accessories",
        "Monitor": "Electronics"
    }

    df_grouped["category"] = df_grouped["product"].map(category_map)

    st.session_state.stock_df = df_grouped
    st.session_state.stock = df_grouped.set_index("product")["quantity"].to_dict()
    st.session_state.sold = {p: 0 for p in st.session_state.stock}

# ------------------ SIDEBAR ------------------
st.sidebar.title("ERP Navigation")

menu = ["Dashboard", "Products"]
if st.session_state.role == "admin":
    menu += [ "Inventory","Stock Upload", "AI Insights"]

page = st.sidebar.radio("Go to", menu)

st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

    st.rerun()

# ------------------ DASHBOARD ------------------
if page == "Dashboard" and st.session_state.role == "admin":
    st.title("📊 ERP Dashboard")
    st.write(f"Welcome **{st.session_state.user}**")

    col1, col2 = st.columns(2)
    col1.metric("Total Quantity Sold", sum(st.session_state.sold.values()))
    col2.metric("Total Quantity In Stock", sum(st.session_state.stock.values()))
elif page == "Dashboard" and st.session_state.role != "admin":
    st.title("📊 ERP Dashboard")
    st.header(f"Welcome **{st.session_state.user}**")
    st.subheader("Buy trusted accessories and electronics easily, with up-to-date stock and seamless ordering.")


# ------------------ INVENTORY ------------------
elif page == "Inventory":
    st.title("📦 Inventory Overview")

    inventory_df = pd.DataFrame({
        "Product": st.session_state.stock.keys(),
        "Quantity Sold": st.session_state.sold.values(),
        "Quantity In Stock": st.session_state.stock.values()
    })

    st.dataframe(inventory_df)

# ------------------ PRODUCTS ------------------
elif page == "Products":
    st.title("🛒 Products")

    for category, group in st.session_state.stock_df.groupby("category"):
        st.subheader(f"📂 {category}")

        for _, row in group.iterrows():
            product = row["product"]
            price = row["price"]

            st.markdown(f"### {product}")
            st.write(f"💰 Price: ₹{price}")
            st.write(f"📦 Stock: {st.session_state.stock[product]}")
            # st.write(f"📊 Sold: {st.session_state.sold[product]}")

            if st.session_state.role == "user" and st.session_state.stock[product] > 0:
                qty = st.number_input(
                    f"Buy Quantity ",
                    min_value=1,
                    max_value=st.session_state.stock[product],
                    key=f"qty_{product}"
                )

                if st.button(f"Buy ", key=f"buy_{product}"):
                    st.session_state.stock[product] -= qty
                    st.session_state.sold[product] += qty

                    st.session_state.orders.append({
                        "Product": product,
                        "Quantity": qty,
                        "Price": price,
                        "Total": qty * price
                    })

                    st.success(f"Purchased {qty} × {product}")
                    st.rerun()

                # if st.session_state.orders:
                #  st.subheader("🧾 My Orders")
                #  st.dataframe(pd.DataFrame(st.session_state.orders))

# ------------------ STOCK UPLOAD ------------------
elif page == "Stock Upload":
    st.title("📥 Stock Upload (Admin)")
    st.dataframe(st.session_state.stock_df)
    st.success("Stock loaded & grouped successfully")
    df = pd.read_csv("erp_sales_data.csv")
    st.dataframe(df)
    
    if st.button("Generate AI Insights"):
     with st.spinner("Analyzing inventory..."):
            st.write("")
            

# ------------------ AI INSIGHTS ------------------
elif page == "AI Insights":
    st.title("🤖 AI Insights")

    ai_df = pd.DataFrame({
        "Product": st.session_state.stock.keys(),
        "Sold": st.session_state.sold.values(),
        "Stock": st.session_state.stock.values()
    })

    prompt= """Predict which product might run out soon
Generate sales insights
Suggest stock reorder levels
        Summarize last week’s performance"""
    result = ask_groq(f"{ai_df.to_csv(index=False)} {prompt}")

    st.write(result)

   

