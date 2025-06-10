#from app.ui.forms.home import EvaluadorUI
from app.ui.forms.login import App
from app.ui.forms.admin_view import AdminView
from app.ui.forms.operative_main import SampleListFrame
from app.ui.forms.results_form import ResultsForm

#EvaluadorUI()
#App()
view = ResultsForm(2)
view.mainloop()