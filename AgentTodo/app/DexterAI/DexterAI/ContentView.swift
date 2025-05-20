import SwiftUI
import UIKit

struct ContentView: View {
    @StateObject private var viewModel = TaskViewModel()
    
    var body: some View {
        ZStack {
            VStack {
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
            
            // Floating Action Button
            VStack {
                Spacer()
                HStack {
                    Spacer()
                    Button(action: {
                        viewModel.onAddNewTaskTapped()
                    }) {
                        Image(systemName: "plus")
                            .font(.title)
                            .foregroundColor(.white)
                            .frame(width: 60, height: 60)
                            .background(Color.blue)
                            .clipShape(RoundedRectangle(cornerRadius: 15))
                            .shadow(radius: 4)
                    }
                    .padding()
                }
            }
        }
        .sheet(isPresented: $viewModel.isEditSheetPresented) {
            NavigationView {
                Form {
                    TextField("Task", text: $viewModel.editingTaskText)
                    
                    HStack {
                        Text("Estimated Time (minutes)")
                        Spacer()
                        TextField("Minutes", text: $viewModel.editingTaskEstimatedTime)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                            .frame(width: 100)
                    }
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
        .sheet(isPresented: $viewModel.isAddSheetPresented) {
            NavigationView {
                Form {
                    Section {
                        TextField("Enter your task...", text: $viewModel.newTaskText)
                            .onChange(of: viewModel.newTaskText) { _ in
                                viewModel.onTaskTextChanged()
                            }
                            .submitLabel(.done)
                            .onSubmit {
                                if !viewModel.newTaskText.isEmpty && !viewModel.hasEstimation && !viewModel.isEstimating {
                                    viewModel.estimateTaskTime()
                                }
                            }
                            
                        if viewModel.isEstimating {
                            HStack {
                                Text("Estimating time...")
                                Spacer()
                                ProgressView()
                            }
                        }
                    }
                    
                    if viewModel.hasEstimation {
                        Section(header: Text("Estimated Time")) {
                            HStack {
                                Text("Minutes")
                                Spacer()
                                TextField("Minutes", text: $viewModel.newTaskEstimatedTime)
                                    .keyboardType(.numberPad)
                                    .multilineTextAlignment(.trailing)
                                    .frame(width: 100)
                            }
                        }
                    }
                }
                .navigationTitle("Add Task")
                .navigationBarItems(
                    leading: Button("Cancel") {
                        viewModel.onAddTaskCancelTapped()
                    },
                    trailing: Button("Add") {
                        viewModel.onAddTaskTapped()
                    }
                    .disabled(viewModel.newTaskText.isEmpty || !viewModel.hasEstimation || viewModel.isLoading)
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


