from mst import NetworkDesigner

def main():
    # --- 1. Define the Traffic Sensor Network (Synthetic City) ---
    # Nodes: 12 Intersections (0-11)
    # Edges: Streets with weights representing distance/cost
    
    # Node mapping for better readability in report
    intersections = {
        0: "Centro", 1: "Norte", 2: "Sur", 3: "Este", 4: "Oeste",
        5: "Hospital", 6: "Universidad", 7: "Estadio", 8: "Parque Ind.",
        9: "Aeropuerto", 10: "Plaza", 11: "Residencial"
    }
    
    g = NetworkDesigner(12)
    
    # Define edges (u, v, weight)
    # A somewhat realistic city layout
    city_edges = [
        (0, 1, 4), (0, 2, 5), (0, 3, 3), (0, 4, 4), # Centro connections
        (1, 5, 6), (1, 6, 7), # Norte -> Hospital, Uni
        (2, 7, 5), (2, 8, 8), # Sur -> Estadio, Parque Ind
        (3, 9, 10), (3, 10, 4), # Este -> Aeropuerto, Plaza
        (4, 11, 6), (4, 5, 5), # Oeste -> Residencial, Hospital
        (5, 6, 3), # Hospital - Uni
        (6, 10, 8), # Uni - Plaza
        (7, 8, 4), # Estadio - Parque Ind
        (8, 9, 7), # Parque Ind - Aeropuerto
        (9, 10, 6), # Aeropuerto - Plaza
        (10, 11, 9), # Plaza - Residencial
        (11, 5, 7), # Residencial - Hospital
        (1, 3, 6), # Norte - Este ring
        (2, 4, 7)  # Sur - Oeste ring
    ]
    
    for u, v, w in city_edges:
        g.add_edge(u, v, w)
        
    print("--- Traffic Sensor Network Design Project ---")
    print(f"Total Nodes: {g.V}")
    print(f"Total Edges Available: {len(city_edges)}")
    
    # --- 2. Calculate MST using Prim and Kruskal ---
    print("\nRunning Prim's Algorithm...")
    prim_edges, prim_cost = g.prim_mst()
    print(f"Prim MST Cost: {prim_cost}")
    
    print("\nRunning Kruskal's Algorithm...")
    kruskal_edges, kruskal_cost = g.kruskal_mst()
    print(f"Kruskal MST Cost: {kruskal_cost}")
    
    # --- 3. Verify Results ---
    if prim_cost == kruskal_cost:
        print("\n✅ SUCCESS: Both algorithms returned the same optimal cost.")
    else:
        print("\n❌ ERROR: Costs do not match!")
        
    # --- 4. Compare with Fully Connected Network ---
    total_network_cost = g.get_total_connection_cost()
    savings = total_network_cost - prim_cost
    savings_percent = (savings / total_network_cost) * 100
    
    print("\n--- Cost Analysis ---")
    print(f"Cost of Full Redundancy (All Streets Wired): {total_network_cost}")
    print(f"Cost of MST (Minimal Connectivity): {prim_cost}")
    print(f"Savings: {savings} ({savings_percent:.2f}%)")
    
    # --- 5. Generate Mermaid Diagram Code ---
    print("\n--- Mermaid Diagram Code (Copy to Report) ---")
    mermaid_code = "graph TD\n"
    
    # Add all edges, style MST edges differently
    mst_set = set()
    for u, v, w in prim_edges:
        mst_set.add(tuple(sorted((u, v))))
        
    for u, v, w in city_edges:
        edge_key = tuple(sorted((u, v)))
        u_name = intersections[u]
        v_name = intersections[v]
        
        if edge_key in mst_set:
            # Thick green line for MST
            mermaid_code += f"    {u_name} ===|{w}| {v_name}\n"
            mermaid_code += f"    linkStyle {len(mermaid_code.splitlines())-2} stroke:#2ecc71,stroke-width:4px;\n"
        else:
            # Thin dotted/gray line for unused edges
            mermaid_code += f"    {u_name} -.-|{w}| {v_name}\n"
            
    print(mermaid_code)

if __name__ == "__main__":
    main()