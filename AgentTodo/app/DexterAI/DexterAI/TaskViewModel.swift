import SwiftUI

struct Task: Identifiable, Codable {
    let id: Int
    let task: String
    var time: Int?
}

class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []
    @Published var newTaskText: String = ""
    @Published var newTaskEstimatedTime: String = ""
    @Published var isLoading = false
    @Published var isEstimating = false
    @Published var hasEstimation = false
    @Published var errorMessage: String?
    @Published var editingTask: Task?
    @Published var isEditSheetPresented = false
    @Published var editingTaskText: String = ""
    @Published var editingTaskEstimatedTime: String = ""
    @Published var isAddSheetPresented = false
    
    private let baseURL = "https://agent-todo-api.onrender.com"
    
    // MARK: - Public Actions
    
    func onAppear() {
        fetchTasks()
    }
    
    func onAddNewTaskTapped() {
        newTaskText = ""
        newTaskEstimatedTime = ""
        hasEstimation = false
        isAddSheetPresented = true
    }
    
    func onAddTaskCancelTapped() {
        isAddSheetPresented = false
        newTaskText = ""
        newTaskEstimatedTime = ""
        hasEstimation = false
    }
    
    func onAddTaskTapped() {
        guard !newTaskText.isEmpty else { return }
        addTask()
        isAddSheetPresented = false
    }
    
    func onTaskTextChanged() {
        // Reset estimation state when task text changes
        if hasEstimation {
            hasEstimation = false
            newTaskEstimatedTime = ""
        }
    }
    
    func estimateTaskTime() {
        guard !newTaskText.isEmpty else { return }
        isEstimating = true
        
        // URL encode the task text for use in a query parameter
        guard let encodedTask = newTaskText.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
              let url = URL(string: "\(baseURL)/estimate?task=\(encodedTask)") else {
            isEstimating = false
            errorMessage = "Failed to create request URL"
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isEstimating = false
                
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                do {
                    let result = try JSONDecoder().decode(EstimatedTimeResponse.self, from: data)
                    self?.newTaskEstimatedTime = "\(result.estimated_time)"
                    self?.hasEstimation = true
                } catch {
                    self?.errorMessage = "Failed to decode estimation"
                }
            }
        }.resume()
    }
    
    func onDeleteTaskTapped(_ task: Task) {
        deleteTask(task)
    }
    
    func onEditTaskTapped(_ task: Task) {
        editingTask = task
        editingTaskText = task.task
        editingTaskEstimatedTime = task.time != nil ? "\(task.time!)" : ""
        isEditSheetPresented = true
    }
    
    func onEditTaskSaveTapped() {
        guard let task = editingTask else { return }
        updateTask(task, newTaskText: editingTaskText)
        isEditSheetPresented = false
    }
    
    func onEditTaskCancelTapped() {
        isEditSheetPresented = false
        editingTask = nil
        editingTaskText = ""
        editingTaskEstimatedTime = ""
    }
    
    // MARK: - Private Business Logic
    
    private func fetchTasks() {
        guard let url = URL(string: "\(baseURL)/tasks") else { return }
        
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                do {
                    let tasks = try JSONDecoder().decode([Task].self, from: data)
                    self?.tasks = tasks.sorted { ($0.time ?? Int.max) < ($1.time ?? Int.max) }
                } catch {
                    self?.errorMessage = "Failed to decode tasks"
                }
            }
        }.resume()
    }
    
    private func addTask() {
        isLoading = true
        
        guard let url = URL(string: "\(baseURL)/tasks") else { return }
        
        var taskData: [String: Any] = ["task": newTaskText]
        
        // Add estimated time if provided and valid
        if !newTaskEstimatedTime.isEmpty, let timeValue = Int(newTaskEstimatedTime) {
            taskData["time"] = timeValue
        }
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: taskData) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                self?.newTaskText = ""
                self?.newTaskEstimatedTime = ""
                self?.hasEstimation = false
                self?.fetchTasks()
            }
        }.resume()
    }
    
    private func deleteTask(_ task: Task) {
        guard let url = URL(string: "\(baseURL)/tasks/\(task.id)") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        URLSession.shared.dataTask(with: request) { [weak self] _, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse,
                   httpResponse.statusCode == 200 {
                    self?.tasks.removeAll { $0.id == task.id }
                } else {
                    self?.errorMessage = "Failed to delete task"
                }
            }
        }.resume()
    }
    
    private func updateTask(_ task: Task, newTaskText: String) {
        guard let url = URL(string: "\(baseURL)/tasks/\(task.id)") else { return }
        
        var updatedTaskData: [String: Any] = ["task": newTaskText]
        
        // Add estimated time if provided and valid
        if !editingTaskEstimatedTime.isEmpty, let timeValue = Int(editingTaskEstimatedTime) {
            updatedTaskData["time"] = timeValue
        }
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: updatedTaskData) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "PUT"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                do {
                    let updatedTask = try JSONDecoder().decode(Task.self, from: data)
                    if let index = self?.tasks.firstIndex(where: { $0.id == task.id }) {
                        self?.tasks[index] = updatedTask
                    }
                } catch {
                    self?.errorMessage = "Failed to decode updated task"
                }
            }
        }.resume()
    }
}

// Response model for the estimation endpoint
struct EstimatedTimeResponse: Decodable {
    let estimated_time: Int
}


