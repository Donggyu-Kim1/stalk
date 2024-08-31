from django.views.generic import TemplateView
import yfinance as yf

class StockIndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        indices = {
            'NASDAQ': '^IXIC',
            'SP_500': '^GSPC',
            'Dow_Jones': '^DJI'
        }
        
        chart_data = {}
        
        for name, symbol in indices.items():
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            
            hist.index = hist.index.strftime('%Y-%m-%d')
            
            chart_data[name] = hist['Close'].to_dict()
        
        context['chart_data'] = chart_data
        return context