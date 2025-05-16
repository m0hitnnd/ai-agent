import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = TaskViewModel()
    
    var body: some View {
        VStack {
            // Task input field
            HStack {
                TextField("Enter your task...", text: $viewModel.newTaskText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Button(action: {
                    viewModel.addTask()
                }) {
                    Text("Add Task")
                }
                .disabled(viewModel.newTaskText.isEmpty || viewModel.isLoading)
            }
            .padding()
            
            // Header row
            HStack {
                Text("Task")
                    .font(.headline)
                    .frame(maxWidth: .infinity, alignment: .leading)
                Text("Estimated Time")
                    .font(.headline)
                    .frame(width: 120, alignment: .trailing)
            }
            .padding(.horizontal)
            
            // Task list
            List(viewModel.tasks) { task in
                HStack {
                    Text(task.task)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    if let estimatedTime = task.time {
                        Text("\(estimatedTime) min")
                            .foregroundColor(.secondary)
                            .frame(width: 120, alignment: .trailing)
                    } else {
                        Text("Calculating...")
                            .foregroundColor(.secondary)
                            .frame(width: 120, alignment: .trailing)
                    }
                }
            }
            
            if viewModel.isLoading {
                ProgressView()
                    .padding()
            }
        }
        //.navigationTitle("DexterAI")
        .alert(item: Binding(
            get: { viewModel.errorMessage.map { AlertItem(message: $0) } },
            set: { _ in viewModel.errorMessage = nil }
        )) { alertItem in
            Alert(title: Text("Error"), message: Text(alertItem.message))
        }
        .onAppear {
            viewModel.fetchTasks()
        }
    }
}

struct AlertItem: Identifiable {
    let id = UUID()
    let message: String
}

#Preview {
    ContentView()
}


