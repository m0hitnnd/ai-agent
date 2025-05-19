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
                    viewModel.onAddTaskTapped()
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
                .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                    Button(role: .destructive) {
                        viewModel.onDeleteTaskTapped(task)
                    } label: {
                        Label("Delete", systemImage: "trash")
                    }
                }
                .swipeActions(edge: .leading, allowsFullSwipe: false) {
                    Button {
                        viewModel.onEditTaskTapped(task)
                    } label: {
                        Label("Edit", systemImage: "pencil")
                    }
                    .tint(.blue)
                }
            }
            
            if viewModel.isLoading {
                ProgressView()
                    .padding()
            }
        }
        .sheet(isPresented: $viewModel.isEditSheetPresented) {
            NavigationView {
                Form {
                    TextField("Task", text: $viewModel.editingTaskText)
                }
                .navigationTitle("Edit Task")
                .navigationBarItems(
                    leading: Button("Cancel") {
                        viewModel.onEditTaskCancelTapped()
                    },
                    trailing: Button("Save") {
                        viewModel.onEditTaskSaveTapped()
                    }
                )
            }
        }
        .alert(item: Binding(
            get: { viewModel.errorMessage.map { AlertItem(message: $0) } },
            set: { _ in viewModel.errorMessage = nil }
        )) { alertItem in
            Alert(title: Text("Error"), message: Text(alertItem.message))
        }
        .onAppear {
            viewModel.onAppear()
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


