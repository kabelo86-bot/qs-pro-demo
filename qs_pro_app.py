
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import json
import io
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="QS Pro - Quantity Surveying Software",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #1f4e79;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1f4e79;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f4e79;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        background-color: #1f4e79;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover {
        background-color: #2c6aa6;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        'project_name': '',
        'client': '',
        'location': '',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'building_type': 'Residential',
        'currency': 'EUR',
        'measurements': {},
        'rates': {},
        'boq_items': []
    }

if 'floor_measurements' not in st.session_state:
    st.session_state.floor_measurements = []

if 'wall_measurements' not in st.session_state:
    st.session_state.wall_measurements = []

if 'roof_measurements' not in st.session_state:
    st.session_state.roof_measurements = []

# Standard industry rates (EUR per unit) - can be customized
DEFAULT_RATES = {
    'Concrete (m³)': 120.00,
    'Steel Reinforcement (kg)': 2.50,
    'Bricks (1000 units)': 450.00,
    'Blocks (1000 units)': 380.00,
    'Cement (50kg bag)': 8.50,
    'Sand (m³)': 35.00,
    'Aggregate (m³)': 40.00,
    'Timber (m³)': 650.00,
    'Roof Tiles (m²)': 45.00,
    'Floor Tiles (m²)': 35.00,
    'Wall Tiles (m²)': 38.00,
    'Paint (Litre)': 18.00,
    'Plaster (m²)': 22.00,
    'Insulation (m²)': 28.00,
    'Windows (m²)': 280.00,
    'Doors (unit)': 350.00,
    'Electrical Points (unit)': 85.00,
    'Plumbing Points (unit)': 120.00,
    'Labour (day)': 220.00
}

# Wastage factors
WASTAGE_FACTORS = {
    'Concrete': 1.05,
    'Steel': 1.03,
    'Bricks': 1.08,
    'Blocks': 1.05,
    'Tiles': 1.10,
    'Paint': 1.15,
    'Timber': 1.10,
    'General': 1.05
}

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("## 🏗️ QS Pro")
st.sidebar.markdown("*Professional Quantity Surveying*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📐 Plan Upload & Measurement", "📊 BOQ Generator", "🧮 Calculators", "📈 Reports & Export"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Project Info")
project_name = st.sidebar.text_input("Project Name", st.session_state.project_data['project_name'])
client_name = st.sidebar.text_input("Client", st.session_state.project_data['client'])
location = st.sidebar.text_input("Location", st.session_state.project_data['location'])
building_type = st.sidebar.selectbox("Building Type", ["Residential", "Commercial", "Industrial", "Mixed-Use"])
currency = st.sidebar.selectbox("Currency", ["EUR", "USD", "GBP", "ZAR"])

st.session_state.project_data['project_name'] = project_name
st.session_state.project_data['client'] = client_name
st.session_state.project_data['location'] = location
st.session_state.project_data['building_type'] = building_type
st.session_state.project_data['currency'] = currency

# ============================================================
# HOME PAGE
# ============================================================

if page == "🏠 Home":
    st.markdown('<div class="main-header">QS Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Quantity Surveying Software</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <h3>📐 Plan Analysis</h3>
        <p>Upload building plans (PDF, JPG, PNG) and calibrate measurements. Extract dimensions manually or via assisted measurement tools.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <h3>📊 Bill of Quantities</h3>
        <p>Auto-generate BOQ from measurements. Categories: Substructure, Superstructure, Finishes, M&E, External Works.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <h3>📈 Reports</h3>
        <p>Export professional PDF reports and Excel BOQs with full cost breakdowns, summaries, and analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🚀 Quick Start Guide")

    with st.expander("Step 1: Upload Your Building Plan", expanded=True):
        st.write("Go to **📐 Plan Upload & Measurement** → Upload your architectural drawings → Set the scale using a known dimension (e.g., a 5m wall).")

    with st.expander("Step 2: Take Measurements"):
        st.write("Use the measurement tools to capture: Floor areas, Wall lengths/areas, Roof dimensions, Opening deductions (doors/windows).")

    with st.expander("Step 3: Generate BOQ"):
        st.write("Navigate to **📊 BOQ Generator** → Review auto-calculated quantities → Adjust rates → Add custom items → Generate final BOQ.")

    with st.expander("Step 4: Export Reports"):
        st.write("Go to **📈 Reports & Export** → Download PDF summary or Excel detailed BOQ for client presentation.")

    st.markdown("---")

    # Project summary card
    if project_name:
        st.markdown(f"""
        <div class="success-box">
        <strong>Current Project:</strong> {project_name}<br>
        <strong>Client:</strong> {client_name}<br>
        <strong>Type:</strong> {building_type}<br>
        <strong>Location:</strong> {location}
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PLAN UPLOAD & MEASUREMENT
# ============================================================

elif page == "📐 Plan Upload & Measurement":
    st.markdown('<div class="section-header">📐 Plan Upload & Measurement</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Plan", "📏 Floor Measurements", "🧱 Wall Measurements", "🏠 Roof Measurements"])

    # TAB 1: UPLOAD
    with tab1:
        st.subheader("Upload Building Plan")
        uploaded_file = st.file_uploader("Upload PDF, JPG, or PNG", type=['pdf', 'jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            file_type = uploaded_file.type

            if file_type in ['image/jpeg', 'image/png', 'image/jpg']:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Plan", use_column_width=True)

                st.markdown("### Scale Calibration")
                st.write("To measure accurately, calibrate using a known dimension on the plan.")

                col1, col2 = st.columns(2)
                with col1:
                    known_length = st.number_input("Known length on plan (e.g., 5.0 meters)", min_value=0.1, value=5.0, step=0.1)
                with col2:
                    pixel_length = st.number_input("Measured in pixels (use image editor or estimate)", min_value=1, value=100, step=1)

                if pixel_length > 0:
                    scale_factor = known_length / pixel_length  # meters per pixel
                    st.session_state.project_data['scale_factor'] = scale_factor
                    st.success(f"Scale calibrated: {scale_factor:.4f} meters per pixel")
                    st.info("💡 Tip: Use the measurement tools below to calculate areas and lengths from your plan.")

            elif file_type == 'application/pdf':
                st.info("PDF uploaded. For PDF plans, convert pages to images or use the manual measurement entry below.")
                st.write("PDF processing would require additional libraries (pdf2image, PyMuPDF). For this prototype, please describe the plan dimensions manually or convert to image.")

    # TAB 2: FLOOR MEASUREMENTS
    with tab2:
        st.subheader("Floor Area Measurements")

        with st.form("floor_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                room_name = st.text_input("Room/Area Name", "Living Room")
            with col2:
                length = st.number_input("Length (m)", min_value=0.0, value=5.0, step=0.1)
            with col3:
                width = st.number_input("Width (m)", min_value=0.0, value=4.0, step=0.1)

            col4, col5 = st.columns(2)
            with col4:
                floor_type = st.selectbox("Floor Type", ["Concrete Slab", "Suspended Floor", "Ground Floor", "Upper Floor", "Basement"])
            with col5:
                finish = st.selectbox("Finish", ["Tiles", "Timber", "Carpet", "Polished Concrete", "Screed Only"])

            submitted = st.form_submit_button("➕ Add Floor Measurement")

            if submitted:
                area = length * width
                st.session_state.floor_measurements.append({
                    'room': room_name,
                    'length': length,
                    'width': width,
                    'area': area,
                    'floor_type': floor_type,
                    'finish': finish
                })
                st.success(f"Added {room_name}: {area:.2f} m²")

        if st.session_state.floor_measurements:
            st.markdown("### Floor Measurements Summary")
            df_floors = pd.DataFrame(st.session_state.floor_measurements)
            st.dataframe(df_floors, use_container_width=True)

            total_floor_area = df_floors['area'].sum()
            st.metric("Total Floor Area", f"{total_floor_area:.2f} m²")

            # Auto-calculate materials
            st.markdown("### Auto-Calculated Floor Materials")

            concrete_vol = total_floor_area * 0.15  # 150mm thick slab assumption
            screed_vol = total_floor_area * 0.05     # 50mm screed
            tiles_area = total_floor_area * 1.10     # 10% wastage

            col1, col2, col3 = st.columns(3)
            col1.metric("Concrete (150mm slab)", f"{concrete_vol:.2f} m³")
            col2.metric("Screed (50mm)", f"{screed_vol:.2f} m³")
            col3.metric("Floor Tiles (incl. 10% wastage)", f"{tiles_area:.2f} m²")

    # TAB 3: WALL MEASUREMENTS
    with tab3:
        st.subheader("Wall Measurements")

        with st.form("wall_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                wall_name = st.text_input("Wall/Room Name", "External Wall - Living Room")
            with col2:
                wall_length = st.number_input("Wall Length (m)", min_value=0.0, value=5.0, step=0.1)
            with col3:
                wall_height = st.number_input("Wall Height (m)", min_value=0.0, value=2.7, step=0.1)

            col4, col5, col6 = st.columns(3)
            with col4:
                wall_type = st.selectbox("Wall Type", ["External Cavity", "External Solid", "Internal Partition", "Load Bearing", "Retaining"])
            with col5:
                construction = st.selectbox("Construction", ["Brick & Block", "Block & Block", "Timber Frame", "Steel Frame", "Concrete"])
            with col6:
                openings = st.number_input("Openings Area (m²)", min_value=0.0, value=0.0, step=0.1, help="Total area of doors/windows in this wall")

            submitted = st.form_submit_button("➕ Add Wall Measurement")

            if submitted:
                gross_area = wall_length * wall_height
                net_area = gross_area - openings
                st.session_state.wall_measurements.append({
                    'wall': wall_name,
                    'length': wall_length,
                    'height': wall_height,
                    'gross_area': gross_area,
                    'openings': openings,
                    'net_area': net_area,
                    'wall_type': wall_type,
                    'construction': construction
                })
                st.success(f"Added {wall_name}: Net area {net_area:.2f} m²")

        if st.session_state.wall_measurements:
            st.markdown("### Wall Measurements Summary")
            df_walls = pd.DataFrame(st.session_state.wall_measurements)
            st.dataframe(df_walls, use_container_width=True)

            total_wall_area = df_walls['net_area'].sum()
            total_gross = df_walls['gross_area'].sum()
            total_openings = df_walls['openings'].sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Gross Wall Area", f"{total_gross:.2f} m²")
            col2.metric("Total Openings", f"{total_openings:.2f} m²")
            col3.metric("Total Net Wall Area", f"{total_wall_area:.2f} m²")

            # Auto-calculate materials
            st.markdown("### Auto-Calculated Wall Materials")

            # Brick calculation: 60 bricks per m² for single leaf, 120 for cavity
            brick_count = total_wall_area * 60  # Simplified single leaf
            block_count = total_wall_area * 10  # 10 blocks per m²
            mortar_vol = total_wall_area * 0.015  # 15mm mortar
            plaster_area = total_wall_area * 2     # Both sides
            paint_area = plaster_area

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Bricks (single leaf, 60/m²)", f"{brick_count:,.0f} units")
            col2.metric("Blocks (10/m²)", f"{block_count:,.0f} units")
            col3.metric("Plaster (both sides)", f"{plaster_area:.2f} m²")
            col4.metric("Paint", f"{paint_area:.2f} m²")

    # TAB 4: ROOF MEASUREMENTS
    with tab4:
        st.subheader("Roof Measurements")

        with st.form("roof_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                roof_section = st.text_input("Roof Section", "Main Roof")
            with col2:
                plan_area = st.number_input("Plan Area (m²)", min_value=0.0, value=50.0, step=0.1)
            with col3:
                pitch = st.number_input("Pitch Angle (degrees)", min_value=0.0, max_value=60.0, value=30.0, step=1.0)

            col4, col5 = st.columns(2)
            with col4:
                roof_type = st.selectbox("Roof Type", ["Pitched Tiled", "Pitched Slate", "Flat Felt", "Flat EPDM", "Metal Standing Seam", "Green Roof"])
            with col5:
                overhang = st.number_input("Eaves Overhang (m)", min_value=0.0, value=0.5, step=0.1)

            submitted = st.form_submit_button("➕ Add Roof Measurement")

            if submitted:
                # Calculate actual roof area based on pitch
                pitch_rad = np.radians(pitch)
                slope_factor = 1 / np.cos(pitch_rad) if pitch > 0 else 1
                actual_area = plan_area * slope_factor

                # Add overhang area (approximate)
                perimeter = np.sqrt(plan_area) * 4  # Rough square assumption
                overhang_area = perimeter * overhang
                total_roof_area = actual_area + overhang_area

                st.session_state.roof_measurements.append({
                    'section': roof_section,
                    'plan_area': plan_area,
                    'pitch': pitch,
                    'slope_factor': slope_factor,
                    'actual_area': actual_area,
                    'overhang_area': overhang_area,
                    'total_area': total_roof_area,
                    'roof_type': roof_type
                })
                st.success(f"Added {roof_section}: {total_roof_area:.2f} m² (slope factor: {slope_factor:.3f})")

        if st.session_state.roof_measurements:
            st.markdown("### Roof Measurements Summary")
            df_roofs = pd.DataFrame(st.session_state.roof_measurements)
            st.dataframe(df_roofs, use_container_width=True)

            total_roof = df_roofs['total_area'].sum()
            st.metric("Total Roof Area", f"{total_roof:.2f} m²")

            # Auto-calculate materials
            st.markdown("### Auto-Calculated Roof Materials")

            tiles_area = total_roof * 1.10  # 10% wastage
            battens_length = total_roof * 2.5  # Approximate
            membrane_area = total_roof * 1.05
            insulation_area = total_roof
            gutter_length = np.sqrt(total_roof) * 4  # Rough estimate

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Roof Tiles (incl. wastage)", f"{tiles_area:.2f} m²")
            col2.metric("Breathable Membrane", f"{membrane_area:.2f} m²")
            col3.metric("Insulation", f"{insulation_area:.2f} m²")
            col4.metric("Guttering (est.)", f"{gutter_length:.2f} m")

# ============================================================
# BOQ GENERATOR
# ============================================================

elif page == "📊 BOQ Generator":
    st.markdown('<div class="section-header">📊 Bill of Quantities Generator</div>', unsafe_allow_html=True)

    # Build BOQ from measurements
    boq_items = []

    # Floor items
    if st.session_state.floor_measurements:
        df_floors = pd.DataFrame(st.session_state.floor_measurements)
        total_floor = df_floors['area'].sum()

        boq_items.extend([
            {'item_no': 'A.1.1', 'description': 'Excavation for foundations', 'unit': 'm³', 'quantity': total_floor * 0.3, 'rate': 45.00, 'category': 'Substructure'},
            {'item_no': 'A.1.2', 'description': 'Concrete bed (150mm thick)', 'unit': 'm³', 'quantity': total_floor * 0.15, 'rate': 120.00, 'category': 'Substructure'},
            {'item_no': 'A.1.3', 'description': 'Hardcore filling and compacting', 'unit': 'm³', 'quantity': total_floor * 0.20, 'rate': 35.00, 'category': 'Substructure'},
            {'item_no': 'A.1.4', 'description': 'Damp proof membrane', 'unit': 'm²', 'quantity': total_floor, 'rate': 8.50, 'category': 'Substructure'},
            {'item_no': 'B.1.1', 'description': 'Floor screed (50mm)', 'unit': 'm²', 'quantity': total_floor, 'rate': 18.00, 'category': 'Superstructure - Floors'},
            {'item_no': 'B.1.2', 'description': 'Floor tiles supply and fix', 'unit': 'm²', 'quantity': total_floor * 1.10, 'rate': 35.00, 'category': 'Superstructure - Floors'},
        ])

    # Wall items
    if st.session_state.wall_measurements:
        df_walls = pd.DataFrame(st.session_state.wall_measurements)
        total_net_wall = df_walls['net_area'].sum()
        total_gross_wall = df_walls['gross_area'].sum()
        total_openings = df_walls['openings'].sum()

        boq_items.extend([
            {'item_no': 'B.2.1', 'description': 'External cavity wall (brick/block)', 'unit': 'm²', 'quantity': total_net_wall, 'rate': 85.00, 'category': 'Superstructure - Walls'},
            {'item_no': 'B.2.2', 'description': 'Internal plaster (two coat)', 'unit': 'm²', 'quantity': total_net_wall * 2, 'rate': 22.00, 'category': 'Finishes'},
            {'item_no': 'B.2.3', 'description': 'Emulsion paint (two coats)', 'unit': 'm²', 'quantity': total_net_wall * 2, 'rate': 12.00, 'category': 'Finishes'},
            {'item_no': 'B.2.4', 'description': 'Windows (UPVC double glazed)', 'unit': 'm²', 'quantity': total_openings * 0.6, 'rate': 280.00, 'category': 'Superstructure - Openings'},
            {'item_no': 'B.2.5', 'description': 'Internal doors (paint grade)', 'unit': 'nr', 'quantity': max(1, int(total_openings * 0.4 / 2)), 'rate': 350.00, 'category': 'Superstructure - Openings'},
        ])

    # Roof items
    if st.session_state.roof_measurements:
        df_roofs = pd.DataFrame(st.session_state.roof_measurements)
        total_roof = df_roofs['total_area'].sum()

        boq_items.extend([
            {'item_no': 'B.3.1', 'description': 'Roof trusses (timber FSC)', 'unit': 'm²', 'quantity': total_roof, 'rate': 65.00, 'category': 'Superstructure - Roof'},
            {'item_no': 'B.3.2', 'description': 'Roof tiles (concrete) supply and fix', 'unit': 'm²', 'quantity': total_roof * 1.10, 'rate': 45.00, 'category': 'Superstructure - Roof'},
            {'item_no': 'B.3.3', 'description': 'Breathable membrane', 'unit': 'm²', 'quantity': total_roof * 1.05, 'rate': 8.00, 'category': 'Superstructure - Roof'},
            {'item_no': 'B.3.4', 'description': 'Roof insulation (150mm)', 'unit': 'm²', 'quantity': total_roof, 'rate': 28.00, 'category': 'Superstructure - Roof'},
            {'item_no': 'B.3.5', 'description': 'Guttering and downpipes (PVC)', 'unit': 'm', 'quantity': np.sqrt(total_roof) * 4, 'rate': 25.00, 'category': 'External Works'},
        ])

    # M&E approximates (based on floor area)
    if st.session_state.floor_measurements:
        df_floors = pd.DataFrame(st.session_state.floor_measurements)
        total_floor = df_floors['area'].sum()

        boq_items.extend([
            {'item_no': 'C.1.1', 'description': 'Electrical installation (1st fix)', 'unit': 'm²', 'quantity': total_floor, 'rate': 45.00, 'category': 'M&E - Electrical'},
            {'item_no': 'C.1.2', 'description': 'Electrical installation (2nd fix)', 'unit': 'm²', 'quantity': total_floor, 'rate': 38.00, 'category': 'M&E - Electrical'},
            {'item_no': 'C.1.3', 'description': 'Light fittings (LED standard)', 'unit': 'nr', 'quantity': max(1, int(total_floor / 12)), 'rate': 85.00, 'category': 'M&E - Electrical'},
            {'item_no': 'C.2.1', 'description': 'Plumbing (1st fix)', 'unit': 'm²', 'quantity': total_floor, 'rate': 35.00, 'category': 'M&E - Plumbing'},
            {'item_no': 'C.2.2', 'description': 'Plumbing (2nd fix - sanitaryware)', 'unit': 'm²', 'quantity': total_floor, 'rate': 42.00, 'category': 'M&E - Plumbing'},
        ])

    # Preliminaries & margin
    if boq_items:
        total_prelim = sum(item['quantity'] * item['rate'] for item in boq_items) * 0.08
        boq_items.append({'item_no': 'D.1.1', 'description': 'Preliminaries (8%)', 'unit': 'sum', 'quantity': 1, 'rate': total_prelim, 'category': 'Preliminaries'})

    # Display BOQ
    if boq_items:
        df_boq = pd.DataFrame(boq_items)
        df_boq['amount'] = df_boq['quantity'] * df_boq['rate']

        # Allow rate editing
        st.markdown("### Review and Adjust Rates")
        st.write("Rates are pre-populated with industry averages. Adjust as needed for your project.")

        edited_df = st.data_editor(
            df_boq[['item_no', 'description', 'unit', 'quantity', 'rate', 'category']],
            column_config={
                "rate": st.column_config.NumberColumn("Rate", min_value=0, format="%.2f"),
                "quantity": st.column_config.NumberColumn("Quantity", min_value=0, format="%.2f"),
            },
            use_container_width=True,
            num_rows="dynamic"
        )

        # Recalculate with edited rates
        edited_df['amount'] = edited_df['quantity'] * edited_df['rate']

        st.markdown("### Bill of Quantities Summary")

        # Category breakdown
        category_summary = edited_df.groupby('category')['amount'].sum().reset_index()
        category_summary = category_summary.sort_values('amount', ascending=False)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.dataframe(category_summary, use_container_width=True)

        with col2:
            total_cost = edited_df['amount'].sum()
            st.metric("Total Project Cost", f"€{total_cost:,.2f}")

            if total_floor > 0:
                cost_per_m2 = total_cost / total_floor
                st.metric("Cost per m²", f"€{cost_per_m2:.2f}")

        # Store for reports
        st.session_state.project_data['boq_items'] = edited_df.to_dict('records')
        st.session_state.project_data['total_cost'] = total_cost

    else:
        st.warning("No measurements found. Please go to 📐 Plan Upload & Measurement and add floor, wall, or roof measurements first.")

# ============================================================
# CALCULATORS
# ============================================================

elif page == "🧮 Calculators":
    st.markdown('<div class="section-header">🧮 QS Calculators</div>', unsafe_allow_html=True)

    calc_type = st.selectbox(
        "Select Calculator",
        ["Area & Volume", "Material Quantities", "Brick/Block Calculator", "Paint Calculator", "Concrete Mix", "Cost Analysis"]
    )

    if calc_type == "Area & Volume":
        st.subheader("Area & Volume Calculator")

        shape = st.selectbox("Shape", ["Rectangle", "Circle", "Triangle", "Trapezoid", "Cylinder", "Sphere"])

        if shape == "Rectangle":
            col1, col2 = st.columns(2)
            with col1:
                length = st.number_input("Length (m)", value=5.0)
            with col2:
                width = st.number_input("Width (m)", value=4.0)
            area = length * width
            st.success(f"Area = {area:.2f} m²")

            depth = st.number_input("Depth/Height (m) - for volume", value=0.0)
            if depth > 0:
                volume = area * depth
                st.success(f"Volume = {volume:.2f} m³")

        elif shape == "Circle":
            radius = st.number_input("Radius (m)", value=2.5)
            area = np.pi * radius ** 2
            circumference = 2 * np.pi * radius
            st.success(f"Area = {area:.2f} m² | Circumference = {circumference:.2f} m")

        elif shape == "Triangle":
            col1, col2 = st.columns(2)
            with col1:
                base = st.number_input("Base (m)", value=4.0)
            with col2:
                height = st.number_input("Height (m)", value=3.0)
            area = 0.5 * base * height
            st.success(f"Area = {area:.2f} m²")

    elif calc_type == "Brick/Block Calculator":
        st.subheader("Brick & Block Calculator")

        wall_area = st.number_input("Wall Area (m²)", value=50.0)

        col1, col2 = st.columns(2)
        with col1:
            brick_size = st.selectbox("Brick Size", ["Standard (215x102.5x65mm)", "Metric (190x90x90mm)", "Large Format"])
        with col2:
            bond = st.selectbox("Bond", ["Stretcher", "English", "Flemish", "Stack"])

        # Standard calculations
        bricks_per_m2 = 60 if brick_size == "Standard (215x102.5x65mm)" else 50
        mortar_per_m2 = 0.015  # m³

        total_bricks = wall_area * bricks_per_m2
        wastage = total_bricks * 0.08
        total_with_wastage = total_bricks + wastage
        mortar_vol = wall_area * mortar_per_m2

        st.markdown("### Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Bricks Required", f"{total_bricks:,.0f}")
        col2.metric("With 8% Wastage", f"{total_with_wastage:,.0f}")
        col3.metric("Mortar (m³)", f"{mortar_vol:.3f}")

        # Cement and sand breakdown
        cement_bags = mortar_vol * 6  # approx 6 bags per m³
        sand_m3 = mortar_vol * 0.8

        st.markdown("### Material Breakdown")
        col1, col2 = st.columns(2)
        col1.metric("Cement (50kg bags)", f"{cement_bags:.1f}")
        col2.metric("Sand (m³)", f"{sand_m3:.3f}")

    elif calc_type == "Paint Calculator":
        st.subheader("Paint Calculator")

        surface_area = st.number_input("Surface Area (m²)", value=100.0)
        coats = st.number_input("Number of Coats", min_value=1, max_value=5, value=2)

        paint_type = st.selectbox("Paint Type", ["Emulsion", "Eggshell", "Gloss", "Masonry", "Primer"])

        coverage_rates = {"Emulsion": 12, "Eggshell": 10, "Gloss": 14, "Masonry": 8, "Primer": 10}
        coverage = coverage_rates[paint_type]

        total_litres = (surface_area * coats) / coverage
        wastage = total_litres * 0.10
        total_with_wastage = total_litres + wastage

        st.metric("Paint Required", f"{total_with_wastage:.1f} Litres")
        st.info(f"Coverage rate: {coverage} m²/Litre per coat")

    elif calc_type == "Concrete Mix":
        st.subheader("Concrete Mix Calculator")

        volume = st.number_input("Required Concrete Volume (m³)", value=5.0)
        mix_ratio = st.selectbox("Mix Ratio", ["C20 (1:2:4)", "C25 (1:1.5:3)", "C30 (1:1:2)", "C40 (1:0.5:1)"])

        ratios = {
            "C20 (1:2:4)": (1, 2, 4, 250),
            "C25 (1:1.5:3)": (1, 1.5, 3, 300),
            "C30 (1:1:2)": (1, 1, 2, 350),
            "C40 (1:0.5:1)": (1, 0.5, 1, 400)
        }

        cement_part, sand_part, agg_part, cement_kg_per_m3 = ratios[mix_ratio]
        total_parts = cement_part + sand_part + agg_part

        cement_vol = volume * (cement_part / total_parts)
        sand_vol = volume * (sand_part / total_parts)
        agg_vol = volume * (agg_part / total_parts)
        cement_kg = volume * cement_kg_per_m3
        cement_bags = cement_kg / 50

        st.markdown("### Mix Quantities")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Cement", f"{cement_kg:.0f} kg ({cement_bags:.1f} bags)")
        col2.metric("Sand", f"{sand_vol:.2f} m³")
        col3.metric("Aggregate", f"{agg_vol:.2f} m³")
        col4.metric("Water", f"{volume * 0.5:.2f} m³")

    elif calc_type == "Cost Analysis":
        st.subheader("Cost Analysis Calculator")

        direct_cost = st.number_input("Direct Costs (Materials + Labour)", value=100000.0)
        overhead_percent = st.number_input("Overhead & Profit (%)", value=15.0)
        contingency_percent = st.number_input("Contingency (%)", value=5.0)

        overhead = direct_cost * (overhead_percent / 100)
        contingency = direct_cost * (contingency_percent / 100)
        total = direct_cost + overhead + contingency

        st.markdown("### Cost Breakdown")
        data = {
            'Item': ['Direct Costs', 'Overhead & Profit', 'Contingency', 'TOTAL'],
            'Amount': [direct_cost, overhead, contingency, total],
            'Percentage': [100, overhead_percent, contingency_percent, (total/direct_cost)*100]
        }
        df_cost = pd.DataFrame(data)
        st.dataframe(df_cost, use_container_width=True)

        st.metric("Total Project Cost", f"€{total:,.2f}")

# ============================================================
# REPORTS & EXPORT
# ============================================================

elif page == "📈 Reports & Export":
    st.markdown('<div class="section-header">📈 Reports & Export</div>', unsafe_allow_html=True)

    if not st.session_state.project_data.get('boq_items'):
        st.warning("No BOQ data found. Please generate a BOQ in the 📊 BOQ Generator section first.")
    else:
        st.subheader("Project Summary Report")

        # Project header
        st.markdown(f"""
        ### {st.session_state.project_data['project_name'] or 'Untitled Project'}
        **Client:** {st.session_state.project_data['client'] or 'N/A'}  
        **Location:** {st.session_state.project_data['location'] or 'N/A'}  
        **Building Type:** {st.session_state.project_data['building_type']}  
        **Date:** {st.session_state.project_data['date']}  
        **Currency:** {st.session_state.project_data['currency']}
        """)

        st.markdown("---")

        # BOQ Table
        df_report = pd.DataFrame(st.session_state.project_data['boq_items'])
        if 'amount' not in df_report.columns:
            df_report['amount'] = df_report['quantity'] * df_report['rate']

        st.dataframe(df_report[['item_no', 'description', 'unit', 'quantity', 'rate', 'amount', 'category']], 
                     use_container_width=True)

        # Summary
        total = df_report['amount'].sum()
        st.metric("Total Project Cost", f"€{total:,.2f}")

        # Category pie chart
        st.markdown("### Cost Breakdown by Category")
        category_data = df_report.groupby('category')['amount'].sum().reset_index()

        import plotly.express as px
        fig = px.pie(category_data, values='amount', names='category', 
                     title='Cost Distribution by Category',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)

        # Export options
        st.markdown("### Export Options")

        col1, col2 = st.columns(2)

        with col1:
            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_report.to_excel(writer, sheet_name='BOQ', index=False)

                # Summary sheet
                summary_data = {
                    'Project Name': [st.session_state.project_data['project_name']],
                    'Client': [st.session_state.project_data['client']],
                    'Location': [st.session_state.project_data['location']],
                    'Building Type': [st.session_state.project_data['building_type']],
                    'Date': [st.session_state.project_data['date']],
                    'Total Cost': [total]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

                category_data.to_excel(writer, sheet_name='Category Summary', index=False)

            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download Excel BOQ",
                data=excel_data,
                file_name=f"BOQ_{st.session_state.project_data['project_name'] or 'Project'}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with col2:
            # CSV export
            csv = df_report.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"BOQ_{st.session_state.project_data['project_name'] or 'Project'}.csv",
                mime="text/csv"
            )

        # Print-friendly report
        st.markdown("---")
        st.markdown("### Print-Friendly Report")

        report_text = f"""
BILL OF QUANTITIES
{'='*60}
Project: {st.session_state.project_data['project_name'] or 'Untitled Project'}
Client: {st.session_state.project_data['client'] or 'N/A'}
Location: {st.session_state.project_data['location'] or 'N/A'}
Building Type: {st.session_state.project_data['building_type']}
Date: {st.session_state.project_data['date']}
Currency: {st.session_state.project_data['currency']}
{'='*60}

"""

        for _, row in df_report.iterrows():
            report_text += f"{row['item_no']:8} {row['description'][:40]:40} {row['unit']:6} {row['quantity']:10.2f} @ {row['rate']:10.2f} = {row['amount']:12.2f}\n"

        report_text += f"""
{'='*60}
TOTAL PROJECT COST: {total:,.2f} {st.session_state.project_data['currency']}
{'='*60}

Prepared by: QS Pro Software
This is a computer-generated document.
"""

        st.text_area("Report Preview", report_text, height=400)

        st.download_button(
            label="📥 Download Text Report",
            data=report_text,
            file_name=f"BOQ_Report_{st.session_state.project_data['project_name'] or 'Project'}.txt",
            mime="text/plain"
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<small>QS Pro v1.0 | Built for Quantity Surveyors</small>", unsafe_allow_html=True)
