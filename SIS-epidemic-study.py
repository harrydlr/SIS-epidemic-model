import networkx as nx
import numpy as np
import random
import multiprocessing
import pickle


# Simulate epidemic propagation given model parameters and network
def epidemic_sim(param):
    ref_network, beta, mu, rho_0, T_max, T_trans = param
    G = ref_network
    # Instantiate infected population rho_0=0.2:
    infection_sample = [random.uniform(0, 1) for i in range(100)]
    infection_list = [infection_sample.index(i) for i in infection_sample if i < rho_0]
    for infected_node in infection_list:
        G.nodes[infected_node]["State"] = "I"
    #
    step_infection_rate = []
    # Start random walk:
    for step in range(T_max):
        # Check states:
        next_infected_nodes = []
        next_recovered_nodes = []
        infection_count = 0
        for node in list(G.nodes):
            if G.nodes[node]["State"] == "I":
                infection_count += 1
                random_mu = random.uniform(0, 1)
                if random_mu < mu:
                    next_recovered_nodes.append(node)
            else:
                for neighbor in G.nodes[node]["Neighbors"]:
                    if G.nodes[neighbor]["State"] == "I":
                        random_mu = random.uniform(0, 1)
                        if random_mu < beta:
                            next_infected_nodes.append(node)
                            break
        # Append infection rate
        infection_rate = infection_count/len(list(G.nodes))
        step_infection_rate.append(infection_rate)
        # Update states:
        for infected_node in next_infected_nodes:
            G.nodes[infected_node]["State"] = "I"
        for recovered_node in next_recovered_nodes:
            G.nodes[recovered_node]["State"] = "S"
    # Compute average of infection rate:
    rho_avg = np.mean(step_infection_rate[-(T_max-T_trans):])
    return rho_avg

# Systematic study of epidemic propagation
def SIS_MC(ref_network, N_rep, rho_0, mu_list, beta_list, T_max, T_trans):
    # Create dictionary of results
    global_results = {}
    for mu in mu_list:
        print(mu)
        global_results[mu] = {}
        for beta in beta_list:
            print(beta)
            rho_avg_list = []
            inputs = [(ref_network, beta, mu, rho_0, T_max, T_trans) for i in range(N_rep)]
            with multiprocessing.Pool(8) as p:
                rho_avg = p.map(epidemic_sim, inputs)
                rho_avg_list.append(rho_avg)
            global_results[mu][beta] = np.mean(rho_avg_list)
    return global_results



# Create/define Network:
ref_network = nx.erdos_renyi_graph(500,0.02)
# Set "State" attribute and initialize all the nodes to State=S
nx.set_node_attributes(ref_network, "S", name="State")
# Create list of neighbors for each node of the network:
nx.set_node_attributes(ref_network, None, name="Neighbors")
for node in list(ref_network.nodes):
    neighbors = [n for n in ref_network[node]]
    ref_network.nodes[node]["Neighbors"] = neighbors
# Set beta and mu grid for the study:
beta_list = np.arange(0, 1.02, 0.02).tolist()
mu_list = [0.1, 0.5, 0.9]
# Define rho_0:
rho_0 = 0.2
# Define repetitions of every simulation:
N_rep = 50
# Define T_max, maximum number of time steps of each simulation:
T_max = 1000
# Define T_trans, number of steps of the transitory:
T_trans = 900
final_results = SIS_MC(ref_network, N_rep, rho_0, mu_list, beta_list, T_max, T_trans)
a_file = open("er-500-0.012", "wb")
pickle.dump(final_results, a_file)
a_file.close()
