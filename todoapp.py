# Εισαγωγή βιβλιοθηκών
import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Συνάρτηση για ανάγνωση todos από το JSON αρχείο
def get_todos():
    with open('todos.json', encoding="utf8") as json_file:
        todos = json.load(json_file)
        return todos

# Συνάρτηση για εύρεση του επόμενου διαθέσιμου ID
def get_next_id():
    todos = get_todos()
    if not todos:  # Αν η λίστα είναι κενή
        return 1
    # Βρίσκει το μεγαλύτερο ID και προσθέτει 1
    max_id = max(todo['id'] for todo in todos)
    return max_id + 1

# Συνάρτηση για προσθήκη νέου todo στη λίστα
def add_todo(todo):
    todos = get_todos()
    # Έλεγχος αν υπάρχει ήδη todo με το ίδιο όνομα (case-insensitive)
    existing_names = [existing_todo['name'].lower().strip() for existing_todo in todos]
    if todo['name'].lower().strip() not in existing_names:
        todos.append(todo)
        with open('todos.json', 'w', encoding="utf8") as json_file:
            return json.dump(todos, json_file, ensure_ascii=False, indent=4)
    # Αν υπάρχει ήδη δεν κάνει τίποτα
    
# Συνάρτηση για αλλαγή κατάστασης todo (completed/not completed)
def changestatus(id):
    todos = get_todos()
    todo = next(filter(lambda t: t['id'] == int(id), todos))
    todo['completed'] = not todo['completed']
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii=False, indent=4)

# Συνάρτηση για διαγραφή todo από τη λίστα
def delete_todo(id):
    todos = get_todos()
    todos = [t for t in filter(lambda t: t['id'] != int(id), todos)]
    with open('todos.json', 'w', encoding="utf8") as json_file:
        return json.dump(todos, json_file, ensure_ascii=False, indent=4)

# Αρχική σελίδα  ανακατεύθυνση στη λίστα todos
@app.route('/')
def home():
    return redirect(url_for('list'))

# Σελίδα με τη λίστα todos
@app.route('/todolist/',methods=['GET', 'POST'])
def list():
    if request.method == 'POST':  # Όταν υποβάλλεται νέο todo
        todo = request.form.get('todoname', '').strip()  # Αφαιρεί κενά από αρχή/τέλος
        # Έλεγχος αν το input είναι κενό ή περιέχει μόνο κενά
        if todo:  # Προσθέτει μόνο αν υπάρχει κείμενο
            todoDict = {
                'id': get_next_id(),  # Νέο ID βάσει διαθέσιμου ID
                'name': todo,
                'completed': False,
                
                }
            add_todo(todoDict)
    return render_template('todolist.html',todos=get_todos())

# Route για αλλαγή κατάστασης todo (checkbox)
@app.route('/changestatus/<int:id>')
def change_status(id):
    changestatus(id)
    return redirect(url_for('list'))

# Route για διαγραφή todo
@app.route('/delete/<int:id>')
def delete_item(id):
    delete_todo(id)
    return redirect(url_for('list'))

# Εκκίνηση της εφαρμογής Flask
if __name__ == '__main__':
    app.run(debug=True)


# ctrl + c to stop the server
# To run the app, use the command: python todoapp.py
# deactivate to stop the virtual environment
# to reactivate env\Scripts\activate.bat