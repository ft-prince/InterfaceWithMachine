from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Screen, Product
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.templatetags.static import static  # Import the static function

@login_required
def display_screen_content(request):
    # Retrieve the logged-in user
    user = request.user

    # Filter Screen objects based on the logged-in user's manager status
    # and related to a Running product
    screens = Screen.objects.filter(manager=user, product__status='RUNNING')

    # Pass the filtered screens to the template
    return render(request, 'screen.html', {'screens': screens})

@login_required
def update_content(request):
    products = Product.objects.all()
    if request.method == 'POST':
        # Handle form submission to update content
        pass  # Add your logic here
    return render(request, 'update_content.html', {'products': products})

@staff_member_required
def activate_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        try:
            product = Product.objects.get(id=product_id)
            product.status = "RUNNING"
            product.save()

            # Set all other products to "Stopped" state
            other_products = Product.objects.exclude(id=product_id)
            for other_product in other_products:
                other_product.status = "STOPPED"
                other_product.save()

            # Redirect to display_screen_content view with the id of the running product
            return redirect('display_screen_content')
        except Product.DoesNotExist:
            # Handle case where selected product does not exist
            pass

    products = Product.objects.all()
    return render(request, 'activate_product.html', {'products': products})

def fetch_updated_video_data(request):
    # Retrieve updated video data from the database (e.g., Screen objects)
    updated_video_data = Screen.objects.filter(manager=request.user, product__status='RUNNING').exclude(video_path__isnull=True)

    # Construct the absolute URLs for the static video files
    serialized_video_data = []
    for screen in updated_video_data:
        video_url = static(screen.video_path)
        serialized_video_data.append({'video_path': video_url})

    # Return the serialized video data as JSON response
    return JsonResponse(serialized_video_data, safe=False)

def fetch_updated_pdf_data(request):
    # Retrieve updated PDF data from the database (e.g., Screen objects)
    updated_pdf_data = Screen.objects.filter(manager=request.user, product__status='RUNNING').exclude(pdf_path__isnull=True)

    # Construct the absolute URLs for the static PDF files
    serialized_pdf_data = []
    for screen in updated_pdf_data:
        pdf_url = static(screen.pdf_path)
        serialized_pdf_data.append({'pdf_path': pdf_url})

    # Return the serialized PDF data as JSON response
    return JsonResponse(serialized_pdf_data, safe=False)

def fetch_updated_data(request):
    # Assuming Screen model has fields video_path and pdf_path
    updated_data = []
    screens = Screen.objects.all()

    for screen in screens:
        updated_data.append({
            'video_path': static(screen.video_path),
            'pdf_path': static(screen.pdf_path),
        })

    return JsonResponse(updated_data, safe=False)


#----------------------------------------------------------------
# FixtureCleaningRecordView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import FixtureCleaningRecord
from .forms import FixtureCleaningRecordForm
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class AddFixtureCleaningRecordView(View):
    def get(self, request):
        form = FixtureCleaningRecordForm()
        return render(request, 'fixture_records/add_fixture_cleaning_record.html', {'form': form})

    def post(self, request):
        form = FixtureCleaningRecordForm(request.POST)
        if form.is_valid():
            fixture_record = form.save(commit=False)  # Create the object but don't save it yet
            fixture_record.operator_name = request.user  # Set the logged-in user as the operator_name
            fixture_record.save()  # Now save the object to the database
            return redirect('add_fixture_cleaning_record')
        return render(request, 'fixture_records/add_fixture_cleaning_record.html', {'form': form})


import csv
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import xlsxwriter
from .models import FixtureCleaningRecord


@method_decorator(staff_member_required, name='dispatch')
class ListFixtureCleaningRecordView(ListView):
    model = FixtureCleaningRecord
    template_name = 'fixture_records/list_fixture_cleaning_records.html'
    context_object_name = 'records'
    ordering = ['-date', '-time']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(fixture_control_no__icontains=search_query) |
                Q(fixture_location__icontains=search_query) |
                Q(shift__icontains=search_query) |
                Q(operator_name__username__icontains=search_query) |
                Q(verification_tag_available__icontains=search_query) |
                Q(verification_tag_condition__icontains=search_query) |
                Q(no_dust_on_fixture__icontains=search_query) |
                Q(no_epoxy_coating_on_fixture__icontains=search_query)
            )
        # Apply filters
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        location = self.request.GET.get('location')
        shift = self.request.GET.get('shift')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if location:
            queryset = queryset.filter(fixture_location__icontains=location)
        if shift:
            queryset = queryset.filter(shift=shift)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['location'] = self.request.GET.get('location', '')
        context['shift'] = self.request.GET.get('shift', '')
        return context

    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            queryset = self.get_queryset()
            export_format = request.GET.get('export')
            if export_format == 'excel':
                return self.export_excel(queryset)
            elif export_format == 'pdf':
                return self.export_pdf(queryset)
        return super().get(request, *args, **kwargs)

    def export_excel(self, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=fixture_cleaning_records.xlsx'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define styles
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#4CAF50',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        date_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd'
        })

        # Set column widths
        worksheet.set_column('A:I', 15)

        # Write header row
        headers = ['Control No', 'Location', 'Shift', 'Date', 'Operator Name', 'Tag Available', 'Tag Condition', 'No Dust', 'No Epoxy Coating']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Write data rows
        for row, record in enumerate(queryset, start=1):
            worksheet.write(row, 0, record.fixture_control_no, cell_format)
            worksheet.write(row, 1, record.fixture_location, cell_format)
            worksheet.write(row, 2, record.shift, cell_format)
            worksheet.write(row, 3, record.date, date_format)
            worksheet.write(row, 4, record.operator_name.username if record.operator_name else '', cell_format)
            worksheet.write(row, 5, record.verification_tag_available, cell_format)
            worksheet.write(row, 6, record.verification_tag_condition, cell_format)
            worksheet.write(row, 7, record.no_dust_on_fixture, cell_format)
            worksheet.write(row, 8, record.no_epoxy_coating_on_fixture, cell_format)

        # Add alternating row colors
        for row in range(1, len(queryset) + 1):
            if row % 2 == 0:
                worksheet.set_row(row, None, workbook.add_format({'bg_color': '#f2f2f2'}))

        workbook.close()
        return response

    def export_pdf(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=fixture_cleaning_records.pdf'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

        elements = []

        # Add title
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Fixture Cleaning Records", styles['Title']))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Prepare data for table
        data = [['Control No', 'Location', 'Shift', 'Date', 'Operator', 'Tag Available', 'Tag Condition', 'No Dust', 'No Epoxy']]
        for record in queryset:
            data.append([
                record.fixture_control_no,
                record.fixture_location,
                record.shift,
                record.date.strftime('%Y-%m-%d'),
                record.operator_name.username if record.operator_name else '',
                record.verification_tag_available,
                record.verification_tag_condition,
                record.no_dust_on_fixture,
                record.no_epoxy_coating_on_fixture
            ])

        # Create table
        table = Table(data)

        # Add style to table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Add a strip pattern to the table
        for row in range(1, len(data)):
            if row % 2 == 0:
                style.add('BACKGROUND', (0, row), (-1, row), colors.lightgrey)

        table.setStyle(style)

        # Add the table to the elements
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

@method_decorator(staff_member_required, name='dispatch')
class UpdateFixtureCleaningRecordView(UpdateView):
    model = FixtureCleaningRecord
    form_class = FixtureCleaningRecordForm
    template_name = 'fixture_records/update_fixture_cleaning_record.html'
    success_url = reverse_lazy('list_fixture_cleaning_records')
    
@method_decorator(staff_member_required, name='dispatch')
class DeleteFixtureCleaningRecordView(DeleteView):
    model = FixtureCleaningRecord
    template_name = 'fixture_records/delete_fixture_cleaning_record.html'
    success_url = reverse_lazy('list_fixture_cleaning_records')

@method_decorator(staff_member_required, name='dispatch')
class FixtureCleaningRecordDetailView(View):
    def get(self, request, pk):
        record = get_object_or_404(FixtureCleaningRecord, pk=pk)
        return render(request, 'fixture_records/fixture_cleaning_record_detail.html', {'record': record})
    


# ----------------------------------------------------------------
# RejectionSheetForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import RejectionSheet
from .forms import RejectionSheetForm



@method_decorator(login_required, name='dispatch')
class AddRejectionSheetView(View):
    def get(self, request):
        form = RejectionSheetForm()
        return render(request, 'Rejection_records/add_rejection_sheet.html', {'form': form})

    def post(self, request):
        form = RejectionSheetForm(request.POST)
        if form.is_valid():
            rejection_sheet = form.save(commit=False)  # Create the object but don't save it yet
            rejection_sheet.operator_name = request.user  # Set the logged-in user as the operator_name
            rejection_sheet.save()  # Now save the object to the database
            return redirect('add_rejection_sheet')
        return render(request, 'Rejection_records/add_rejection_sheet.html', {'form': form})

@method_decorator(staff_member_required, name='dispatch')
class ListRejectionSheetView(ListView):
    model = RejectionSheet
    template_name = 'Rejection_records/list_rejection_sheets.html'
    context_object_name = 'sheets'
    ordering = ['-month', '-date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(station__icontains=search_query) |
                Q(stage__icontains=search_query) |
                Q(part_description__icontains=search_query) |
                Q(operator_name__icontains=search_query)
            )

        # Apply filters
        month_from = self.request.GET.get('month_from')
        month_to = self.request.GET.get('month_to')
        station = self.request.GET.get('station')
        stage = self.request.GET.get('stage')

        if month_from:
            queryset = queryset.filter(month__gte=month_from)
        if month_to:
            queryset = queryset.filter(month__lte=month_to)
        if station:
            queryset = queryset.filter(station__icontains=station)
        if stage:
            queryset = queryset.filter(stage__icontains=stage)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['month_from'] = self.request.GET.get('month_from', '')
        context['month_to'] = self.request.GET.get('month_to', '')
        context['station'] = self.request.GET.get('station', '')
        context['stage'] = self.request.GET.get('stage', '')
        return context

@method_decorator(staff_member_required, name='dispatch')
class UpdateRejectionSheetView(UpdateView):
    model = RejectionSheet
    form_class = RejectionSheetForm
    template_name = 'Rejection_records/update_rejection_sheet.html'
    success_url = reverse_lazy('list_rejection_sheets')

@method_decorator(staff_member_required, name='dispatch')
class DeleteRejectionSheetView(DeleteView):
    model = RejectionSheet
    template_name = 'Rejection_records/delete_rejection_sheet.html'
    success_url = reverse_lazy('list_rejection_sheets')

@method_decorator(staff_member_required, name='dispatch')
class RejectionSheetDetailView(View):
    def get(self, request, pk):
        sheet = get_object_or_404(RejectionSheet, pk=pk)
        return render(request, 'Rejection_records/rejection_sheet_detail.html', {'sheet': sheet})
    

    
#----------------------------------------------------------------
# SolderingBitRecord 

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import SolderingBitRecord
from .forms import SolderingBitRecordForm




@method_decorator(login_required, name='dispatch')
class AddSolderingBitRecordView(View):
    def get(self, request):
        form = SolderingBitRecordForm()
        return render(request, 'SolderingBitRecord/add_soldering_bit_record.html', {'form': form})

    def post(self, request):
        form = SolderingBitRecordForm(request.POST)
        if form.is_valid():
            soldering_record = form.save(commit=False)
            soldering_record.operator_name = request.user  # Automatically set the operator name
            soldering_record.save()
            return redirect('add_soldering_bit_record')
        return render(request, 'SolderingBitRecord/add_soldering_bit_record.html', {'form': form})

@method_decorator(staff_member_required, name='dispatch')
class ListSolderingBitRecordView(ListView):
    model = SolderingBitRecord
    template_name = 'SolderingBitRecord/list_soldering_bit_records.html'
    context_object_name = 'records'
    ordering = ['-month']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(doc_number__icontains=search_query) |
                Q(machine_no__name__icontains=search_query) |
                Q(machine_location__icontains=search_query) |
                Q(part_name__icontains=search_query) |
                Q(station__icontains=search_query)
            )
        
        # Apply date filter
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(month__gte=date_from)
        if date_to:
            queryset = queryset.filter(month__lte=date_to)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context

    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            queryset = self.get_queryset()
            export_format = request.GET.get('export')
            if export_format == 'excel':
                return self.export_excel(queryset)
            elif export_format == 'pdf':
                return self.export_pdf(queryset)
        return super().get(request, *args, **kwargs)

    def export_excel(self, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=soldering_bit_records.xlsx'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define styles
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#4CAF50',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        date_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd'
        })
        time_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'hh:mm:ss'
        })

        # Set column widths
        for col in range(17):
            worksheet.set_column(col, col, 15)

        # Write header row
        headers = [
            'Station', 'Doc. No.', 'Part Name', 'Process/Operation', 'Machine Location',
            'Month', 'Time', 'Operator Name', 'Soldering Points/Part', 'Bit Size',
            'Date', 'Produce Quantity Shift A', 'Produce Quantity Shift B',
            'Total Quantity', 'Total Soldering Points/Day', 'Bit Life Remaining',
            'Bit Change Date'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Write data rows
        for row, record in enumerate(queryset, start=1):
            worksheet.write(row, 0, record.station, cell_format)
            worksheet.write(row, 1, record.doc_number, cell_format)
            worksheet.write(row, 2, record.part_name, cell_format)
            worksheet.write(row, 3, record.machine_no.name, cell_format)
            worksheet.write(row, 4, record.get_machine_location_display(), cell_format)
            worksheet.write(row, 5, record.month, date_format)
            worksheet.write(row, 6, record.time, time_format)
            worksheet.write(row, 7, record.operator_name.username if record.operator_name else '', cell_format)
            worksheet.write(row, 8, record.soldering_points_per_part, cell_format)
            worksheet.write(row, 9, record.bit_size, cell_format)
            worksheet.write(row, 10, record.date, date_format)
            worksheet.write(row, 11, record.produce_quantity_shift_a, cell_format)
            worksheet.write(row, 12, record.produce_quantity_shift_b, cell_format)
            worksheet.write(row, 13, record.total_quantity, cell_format)
            worksheet.write(row, 14, record.total_soldering_points, cell_format)
            worksheet.write(row, 15, record.bit_life_remaining, cell_format)
            worksheet.write(row, 16, record.bit_change_date, date_format)

        workbook.close()
        return response

    def export_pdf(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=soldering_bit_records.pdf'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

        elements = []

        # Add title
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Soldering Bit Records", styles['Title']))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Prepare data for table
        data = [
            ['Station', 'Doc. No.', 'Part Name', 'Process/Operation', 'Machine Location',
             'Month', 'Time', 'Operator Name', 'Soldering Points/Part', 'Bit Size',
             'Date', 'Produce Quantity Shift A', 'Produce Quantity Shift B',
             'Total Quantity', 'Total Soldering Points/Day', 'Bit Life Remaining',
             'Bit Change Date']
        ]
        for record in queryset:
            data.append([
                record.station,
                record.doc_number,
                record.part_name,
                record.machine_no.name,
                record.get_machine_location_display(),
                record.month.strftime('%Y-%m-%d'),
                record.time.strftime('%H:%M:%S'),
                record.operator_name.username if record.operator_name else '',
                str(record.soldering_points_per_part),
                record.bit_size,
                record.date.strftime('%Y-%m-%d'),
                str(record.produce_quantity_shift_a),
                str(record.produce_quantity_shift_b),
                str(record.total_quantity),
                str(record.total_soldering_points),
                str(record.bit_life_remaining),
                record.bit_change_date.strftime('%Y-%m-%d')
            ])

        # Create table
        table = Table(data, repeatRows=1)

        # Add style to table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Add a strip pattern to the table
        for row in range(1, len(data)):
            if row % 2 == 0:
                style.add('BACKGROUND', (0, row), (-1, row), colors.lightgrey)

        table.setStyle(style)

        # Add the table to the elements
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    
@method_decorator(staff_member_required, name='dispatch')
class UpdateSolderingBitRecordView(UpdateView):
    model = SolderingBitRecord
    form_class = SolderingBitRecordForm
    template_name = 'SolderingBitRecord/update_soldering_bit_record.html'
    success_url = reverse_lazy('list_soldering_bit_records')
    
@method_decorator(staff_member_required, name='dispatch')
class DeleteSolderingBitRecordView(DeleteView):
    model = SolderingBitRecord
    template_name = 'SolderingBitRecord/delete_soldering_bit_record.html'
    success_url = reverse_lazy('list_soldering_bit_records')

class SolderingBitRecordDetailView(View):
    def get(self, request, pk):
        record = get_object_or_404(SolderingBitRecord, pk=pk)
        return render(request, 'SolderingBitRecord/soldering_bit_record_detail.html', {'record': record})
    
#----------------------------------------------------------------
 

from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import DailyChecklistItem ,WeeklyChecklistItem ,MonthlyChecklistItem
from .forms import DailyChecklistItemForm,WeeklyChecklistItemForm ,MonthlyChecklistItemForm

from django.views import View
from django.shortcuts import render, redirect
from .forms import DailyChecklistItemForm



@method_decorator(login_required, name='dispatch')
class AddDailyChecklistItem(View):
    def get(self, request):
        form = DailyChecklistItemForm()
        return render(request, 'Maintenance/Daily/add_daily.html', {'form': form})

    def post(self, request):
        form = DailyChecklistItemForm(request.POST)

        # Fetch user skill level
        try:
            profile = Profile.objects.get(user=request.user)
            user_skill_level = profile.my_skill
        except Profile.DoesNotExist:
            user_skill_level = 0  # Default skill level if no profile exists
        
        if form.is_valid():
            daily_checklist_item = form.save(commit=False)  # Do not save to the database yet

            # Check skill level against the form's requirements
            # Ensure 'machine_location' and 'min_skill_required' are correctly referenced
            if daily_checklist_item.machine_location.min_skill_required > user_skill_level:
                form.add_error('machine_location', 'Your skill level is insufficient for the selected option.')
                messages.error(request, 'Your skill level is insufficient for the selected option.')
            else:
                try:
                    daily_checklist_item.manager = request.user  # Set the manager to the logged-in user
                    daily_checklist_item.save()  # Save the instance to the database
                    messages.success(request, 'Daily checklist item added successfully.')
                    return redirect('add_daily')  # Ensure this URL name is correct
                except Exception as e:
                    messages.error(request, f'Error saving checklist item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'Maintenance/Daily/add_daily.html', {'form': form})


# ----------------------------------------------------------------
# Without Date filetring 

# from django.db.models import Q
# from django.utils.dateparse import parse_date

# class ListDailyChecklistItem(ListView):
#     model = DailyChecklistItem
#     template_name = 'Maintenance/Daily/list_daily.html'
#     context_object_name = 'records'
#     ordering = ['-month_year']
  

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(doc_number__icontains=query) | 
#                 Q(machine_name__icontains=query) |
#                 Q(machine_location__icontains=query) |
#                 Q(month_year__icontains=query)            
#                 )
#         return queryset


#  With date filetering
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.views.generic import ListView

@method_decorator(staff_member_required, name='dispatch')
class ListDailyChecklistItem(ListView):
    model = DailyChecklistItem
    template_name = 'Maintenance/Daily/list_daily.html'
    context_object_name = 'records'
    ordering = ['-month_year']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        date_query = self.request.GET.get('date')

        if query:
            queryset = queryset.filter(
                Q(doc_number__icontains=query) |
                Q(machine_name__icontains=query) |
                Q(machine_location__icontains=query) |
                Q(month_year__icontains=query)
            )

        if date_query:
            try:
                date = parse_date(date_query)  # Convert the date string to a date object
                if date:
                    queryset = queryset.filter(date=date)
            except ValueError:
                # Handle invalid date format if needed
                pass

        return queryset



#----------------------------------------------------------------

#  with ending and starting date




# from django.db.models import Q
# from django.utils.dateparse import parse_date
# from django.views.generic import ListView

# class ListDailyChecklistItem(ListView):
#     model = DailyChecklistItem
#     template_name = 'Maintenance/Daily/list_daily.html'
#     context_object_name = 'records'
#     ordering = ['-month_year']

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get('q')
#         start_date = self.request.GET.get('start_date')
#         end_date = self.request.GET.get('end_date')

#         if query:
#             queryset = queryset.filter(
#                 Q(doc_number__icontains=query) |
#                 Q(machine_name__icontains=query) |
#                 Q(machine_location__icontains=query) |
#                 Q(month_year__icontains=query)
#             )

#         if start_date and end_date:
#             try:
#                 start_date = parse_date(start_date)
#                 end_date = parse_date(end_date)
#                 if start_date and end_date:
#                     queryset = queryset.filter(date__range=(start_date, end_date))
#             except ValueError:
#                 # Handle invalid date format if needed
#                 pass

#         return queryset










@method_decorator(staff_member_required, name='dispatch')
class UpdateDailyChecklistItem(UpdateView):
    model = DailyChecklistItem
    form_class = DailyChecklistItemForm
    template_name = 'Maintenance/Daily/update_daily.html'
    success_url = reverse_lazy('list_daily')

@method_decorator(staff_member_required, name='dispatch')
class DeleteDailyChecklistItem(DeleteView):
    model = DailyChecklistItem
    template_name = 'Maintenance/Daily/delete_daily.html'
    success_url = reverse_lazy('list_daily')

@method_decorator(staff_member_required, name='dispatch')
class DailyChecklistItemDetailView(View):
    def get(self, request, pk):
        record = get_object_or_404(DailyChecklistItem, pk=pk)
        return render(request, 'Maintenance/Daily/daily_detail.html', {'record': record})

    



#  Weekly Checklist
@method_decorator(login_required, name='dispatch')
class AddWeeklyChecklistItem(View):
    def get(self, request):
        form = WeeklyChecklistItemForm()
        return render(request, 'Maintenance/weekly/add_weekly.html', {'form': form})

    def post(self, request):
        form = WeeklyChecklistItemForm(request.POST)
        
        try:
            profile = Profile.objects.get(user=request.user)
            user_skill_level = profile.my_skill
        except Profile.DoesNotExist:
            user_skill_level = 0  # Default skill level if no profile exists
        
        if form.is_valid():
            monthly_checklist_item = form.save(commit=False)  # Do not save to the database yet

            # Check skill level against the form's requirements
            if monthly_checklist_item.machine_location.min_skill_required > user_skill_level:
                form.add_error('machine_location', 'Your skill level is insufficient for the selected Machine Location.')
                messages.error(request, 'Your skill level is insufficient for the selected Machine Location.')
            else:
                try:
                    monthly_checklist_item.manager = request.user  # Set the manager to the logged-in user
                    monthly_checklist_item.save()  # Save the instance to the database
                    messages.success(request, 'Monthly checklist item added successfully.')
                    return redirect('add_monthly')  # Make sure this URL name is correct
                except Exception as e:
                    messages.error(request, f'Error saving checklist item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'Maintenance/weekly/add_weekly.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class ListWeeklyChecklistItem(ListView):
    model = WeeklyChecklistItem
    template_name = 'Maintenance/weekly/list_weekly.html'
    context_object_name = 'records'
    ordering = ['-month_year']

@method_decorator(staff_member_required, name='dispatch')
class UpdateWeeklyChecklistItem(UpdateView):
    model = WeeklyChecklistItem
    form_class = WeeklyChecklistItemForm
    template_name = 'Maintenance/weekly/update_weekly.html'
    success_url = reverse_lazy('list_weekly')


@method_decorator(staff_member_required, name='dispatch')
class DeleteWeeklyChecklistItem(DeleteView):
    model = WeeklyChecklistItem
    template_name = 'Maintenance/weekly/delete_weekly.html'
    success_url = reverse_lazy('list_weekly')


@method_decorator(staff_member_required, name='dispatch')
class WeeklyChecklistItemDetailView(View):
    def get(self, request, pk):
        record = get_object_or_404(WeeklyChecklistItem, pk=pk)
        return render(request, 'Maintenance/weekly/weekly_detail.html', {'record': record})


# Monthly

@method_decorator(login_required, name='dispatch')
class AddMonthlyChecklistItem(View):
    def get(self, request):
        form = MonthlyChecklistItemForm()
        return render(request, 'Maintenance/monthly/add_monthly.html', {'form': form})

    def post(self, request):
        form = MonthlyChecklistItemForm(request.POST)
        # Fetch user skill level
        try:
            profile = Profile.objects.get(user=request.user)
            user_skill_level = profile.my_skill
        except Profile.DoesNotExist:
            user_skill_level = 0  # Default skill level if no profile exists
        
        if form.is_valid():
            monthly_checklist_item = form.save(commit=False)  # Do not save to the database yet
            
            # Check skill level against the form's requirements
            if monthly_checklist_item.machine_location.min_skill_required > user_skill_level:
                form.add_error(None, 'Your skill level is insufficient for the selected Machine Location.')
                messages.error(request, 'Your skill level is insufficient for the selected Machine Location.')
            else:
                monthly_checklist_item.manager = request.user  # Set the manager to the logged-in user
                try:
                    monthly_checklist_item.save()  # Save the instance to the database
                    messages.success(request, 'Monthly checklist item added successfully.')
                    return redirect('add_monthly')  # Make sure this URL name is correct
                except Exception as e:
                    messages.error(request, f'Error saving checklist item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'Maintenance/monthly/add_monthly.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class ListMonthlyChecklistItem(ListView):
    model = MonthlyChecklistItem
    template_name = 'Maintenance/monthly/list_monthly.html'
    context_object_name = 'records'
    ordering = ['-month_year']


@method_decorator(staff_member_required, name='dispatch')
class UpdateMonthlyChecklistItem(UpdateView):
    model = MonthlyChecklistItem
    form_class = MonthlyChecklistItemForm
    template_name = 'Maintenance/monthly/update_monthly.html'
    success_url = reverse_lazy('list_monthly')


@method_decorator(staff_member_required, name='dispatch')
class DeleteMonthlyChecklistItem(DeleteView):
    model = MonthlyChecklistItem
    template_name = 'Maintenance/monthly/delete_monthly.html'
    success_url = reverse_lazy('list_monthly')


@method_decorator(staff_member_required, name='dispatch')
class MonthlyChecklistItemDetailView(View):
    def get(self, request, pk):
        record = get_object_or_404(MonthlyChecklistItem, pk=pk)
        return render(request, 'Maintenance/monthly/monthly_detail.html', {'record': record})











# ----------------------------------------------------------------



from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ControlChartReading, ControlChartStatistics
from .forms import ControlChartReadingForm

class ReadingListView(ListView):
    model = ControlChartReading
    context_object_name = 'readings'
    template_name = 'reading_list.html'
    ordering = ['-date']

class ReadingDetailView(DetailView):
    model = ControlChartReading
    context_object_name = 'reading'
    template_name = 'reading_detail.html'

class ReadingCreateView(CreateView):
    model = ControlChartReading
    form_class = ControlChartReadingForm
    template_name = 'reading_form.html'
    success_url = reverse_lazy('reading_create')

class ReadingUpdateView(UpdateView):
    model = ControlChartReading
    form_class = ControlChartReadingForm
    template_name = 'reading_form.html'
    success_url = reverse_lazy('reading_list')

class ReadingDeleteView(DeleteView):
    model = ControlChartReading
    context_object_name = 'reading'
    template_name = 'reading_confirm_delete.html'
    success_url = reverse_lazy('reading_list')

from django.shortcuts import render
from .models import ControlChartReading, ControlChartStatistics
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import ControlChartReading, ControlChartStatistics

def control_chart(request):
    # Fetch readings and statistics
    readings = ControlChartReading.objects.all()
    statistics = ControlChartStatistics.objects.all()
    
    # Debug prints
    print(f"Number of readings: {readings.count()}")
    print(f"Number of statistics: {statistics.count()}")
    
    # Calculate control limits
    try:
        control_limits = ControlChartStatistics.calculate_control_limits()
        print("Control limits:", control_limits)
    except Exception as e:
        print(f"Error calculating control limits: {e}")
        control_limits = {}

    # Calculate capability indices
    try:
        capability_indices = ControlChartStatistics.calculate_capability_indices(usl=375, lsl=355)
        print("Capability indices:", capability_indices)
    except Exception as e:
        print(f"Error calculating capability indices: {e}")
        capability_indices = {}

    # Pass context to template
    context = {
        'readings': readings,
        'statistics': statistics,
        'control_limits': control_limits,
        'capability_indices': capability_indices,
    }
    return render(request, 'control_chart.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



from django.shortcuts import render

def index(request):
    return render(request, 'index.html')






from django.template.defaulttags import register

@register.filter
def index(indexable, i):
    return indexable[i]


# ----------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import StartUpCheckSheet
from .forms import StartUpCheckSheetForm

# ListView to display all StartUpCheckSheet entries
class StartUpCheckSheetListView(ListView):
    model = StartUpCheckSheet
    template_name = 'startup/startup_checksheet_list.html'  # Create this template
    context_object_name = 'check_sheets'

# CreateView to create a new StartUpCheckSheet entry
from django.contrib import messages
from .forms import StartUpCheckSheetForm
from user_app.models import Profile
from .models import StartUpCheckSheet, MachineLocation
from django.views.decorators.http import require_http_methods



@require_http_methods(["GET", "POST"])
def startup_checksheet_create_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        user_skill_level = profile.my_skill
    except Profile.DoesNotExist:
        user_skill_level = 0  # Default skill level if no profile exists
    
    if request.method == 'POST':
        form = StartUpCheckSheetForm(request.POST)
        if form.is_valid():
      
            process_operation = form.cleaned_data['process_operation']
            if user_skill_level < process_operation.min_skill_required:
                form.add_error('process_operation', 'Your skill level is not sufficient for this operation.')
                messages.error(request, 'Your skill level is not sufficient for this operation.')
            else:
                try:
                    checksheet = form.save(commit=False)
                    checksheet.manager = request.user                
                # Handle the dynamic checkpoint fields
                    for i in range(1, 26):  # Assuming 25 checkpoints
                        checkpoint_key = f'checkpoint_{i}'
                        if checkpoint_key in request.POST:
                            setattr(checksheet, checkpoint_key, request.POST[checkpoint_key])
                    
                    checksheet.save()
                    messages.success(request, 'Check sheet created successfully.')
                    return redirect('checksheet_create')  # Make sure this URL name is correct
                except Exception as e:
                    messages.error(request, f'Error saving check sheet: {str(e)}')
        else:
                messages.error(request, 'Please correct the errors below.')
    else:
            form = StartUpCheckSheetForm()

    # Prepare checkpoint fields
    checkpoint_fields = [form[f'checkpoint_{i}'] for i in range(1, 26)]  # Assuming 25 checkpoints

    # Replace this with your actual data source
    json_data = [
    {
        "s_no": 1,
        "checkpoint": "Plan के अनसु ार Part assy & Child parts Working Table पर रखें| प्लान के अनसु ार | visual प्रतिदिन",
        "specification": "Part assy & Child parts",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 2,
        "checkpoint": "अपनेकार्स्य थल को साफ करे| कार्स्य थल धलू रदिि िोना चादिए | visual प्रतिदिन",
        "specification": "साफ करे",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 3,
        "checkpoint": "कार्यकरनेसेपिलेWorking table पर सेअनावश्र्क Part / material िटा िें, और उसेउसकी जगि पर रखें| अनावश्र्क Part / material Working Table पर ना िों | visual प्रतिदिन",
        "specification": "Working table पर सेअनावश्र्क Part / material िटा िें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 4,
        "checkpoint": "Dirty tray को लाइन पर use ना करेउसको उसकी तनधायररि जगि पर सफाई के ललए रख िे| Dirty Tray Area visual प्रतिदिन",
        "specification": "Dirty tray को लाइन पर use ना करेउसको उसकी तनधायररि जगि पर सफाई के ललए रख िे",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 5,
        "checkpoint": "चके करेंकक Fixture / Machine Condition OK िों और उसके सभी Connections ठीक िों, Loose ना िों | Fixture / Machine Condition OK, No loose connections visual प्रतिदिन",
        "specification": "Fixture / Machine Condition OK",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 6,
        "checkpoint": "चके करेंकक Fixture / Machine मेंलगेCalibration / Verification Tag की Date Expire ना िों | Verification Tag / Calibration Tag visual प्रतिदिन",
        "specification": "Calibration / Verification Tag की Date Expire ना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 7,
        "checkpoint": "चके करेंकक ESD Wrist Band OK िों | (Where Applicable) लाल / िरा SIGNAL (As per Work instruction) Wrist Band tester प्रतिदिन",
        "specification": "ESD Wrist Band OK",
        "control_method": "Wrist Band tester",
        "frequency": "daily"
    },
    {
        "s_no": 8,
        "checkpoint": "ESD wrist band पिनें| (Where Applicable) कार्यकरिेसमर् Visual प्रतिदिन",
        "specification": "ESD wrist band पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 9,
        "checkpoint": "Face mask पिनें| (Where Applicable) Shop Floor पर उपलब्ध िों| (As per Work instruction) visual प्रतिदिन",
        "specification": "Face mask पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 10,
        "checkpoint": "ESD Jacket & Cap, ESD Gloves/Finger coats पिनें| कार्यकरिेसमर् Visual प्रतिदिन",
        "specification": "ESD Jacket & Cap, ESD Gloves/Finger coats",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 11,
        "checkpoint": "चके करेंकक Red Drawer मेंNG Parts रखनेके ललए Tray उपलब्ध िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Red Drawer मेंNG Parts रखनेके ललए Tray उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 12,
        "checkpoint": "चके करेंकक Drawer मेंजरूरि के अनसु ी र सभी टैग & PPE's उपलब्ध िों | Reject Tag, OK Tag, Abnormal Situation Tag etc. visual प्रतिदिन",
        "specification": "Drawer मेंजरूरि के अनसु ी र सभी टैग & PPE's उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 13,
        "checkpoint": "चके करेंकक Drawer मेंकोई भी अनपुर्ोगी वस्िुना िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Drawer मेंकोई भी अनपुर्ोगी वस्िुना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 14,
        "checkpoint": "चके करेंकक कार्स्य थल पर जरुरि के अनसु ी र सभी Documents उपलब्ध िों | Setup & FPA, Daily monthly Rejection sheet,Control Charts etc. visual प्रतिदिन",
        "specification": "कार्स्य थल पर जरुरि के अनसु ी र सभी Documents उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 15,
        "checkpoint": "चके करेंकक Line पर OK/NG Master sample उपलब्ध िो और उसकी Date Expire ना िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Line पर OK/NG Master sample उपलब्ध िो",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 16,
        "checkpoint": "Tea Break और Lunch मेंबािर जािेसमर् अपनेSetup / System को OFF करके जाएँ| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break और Lunch मेंबािर जािेसमर् अपनेSetup / System को OFF करके जाएँ",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 17,
        "checkpoint": "Tea Break और Lunch मेंबािर जािेसमर् LIGHT को OFF करके जाएँ| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break और Lunch मेंबािर जािेसमर् LIGHT को OFF करके जाएँ",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 18,
        "checkpoint": "Tea Break & Lunch मेंर्दि Shop Floor के अन्िर िैंिो Jacket & Cap पिन कर रखें| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break & Lunch मेंर्दि Shop Floor के अन्िर िैंिो Jacket & Cap पिन कर रखें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 19,
        "checkpoint": "FRL (Pressure gauge) मेंलगी Pin को Push करके 10~12 Sec िक Air को तनकालें, र्दि Air के साथ साथ पानी भी आ रिा िो िो िरुंि अपनेसपु रवाइजर को सचूचि करें| (Where FRL Applicable) OK/NG Visual / Manual प्रतिदिन",
        "specification": "FRL (Pressure gauge) मेंलगी Pin को Push करके 10~12 Sec िक Air को तनकालें, र्दि Air के साथ साथ पानी भी आ रिा िो िो िरुंि अपनेसपु रवाइजर को सचूचि करें",
        "control_method": "Visual / Manual",
        "frequency": "daily"
    },
    {
        "s_no": 20,
        "checkpoint": "चके करेंकक ररजेक्ट िुए Parts के Hand over का िरीका सिी िों | OK/NG सपु रवाइजर के द्वारा प्रतिदिन",
        "specification": "ररजेक्ट िुए Parts के Hand over का िरीका सिी िों",
        "control_method": "Supervisor's verification",
        "frequency": "daily"
    },
    {
        "s_no": 21,
        "checkpoint": "ESD Shoes/Sleepers पिनें| (Where Applicable) Shop Floor पर उपलब्ध िों | visual प्रतिदिन",
        "specification": "ESD Shoes/Sleepers पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 22,
        "checkpoint": "Skill level Card को चके करेंकक उसकी Valid Date Expire ना िों | Shop Floor पर उपलब्ध िों और Valid Date Expire ना िों | visual प्रतिदिन",
        "specification": "Skill level Card को चके करेंकक उसकी Valid Date Expire ना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 23,
        "checkpoint": "चके करेंकक ESD Shoes / Sleepers OK िों | (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "ESD Shoes / Sleepers OK",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 24,
        "checkpoint": "चके करेंकक िर लशफ्ट मेंकार्यशरू करनेसेपिले POGO Pins की ठीक सेसफाई करें| (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "िर लशफ्ट मेंकार्यशरू करनेसेपिले POGO Pins की ठीक सेसफाई करें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 25,
        "checkpoint": "कार्यशरू करनेसेपिलेCuring Rack की condition चके करेंकक Timer सेसेटििों और रैक Damage ना िों | (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "Curing Rack की condition चके करेंकक Timer सेसेटििों और रैक Damage ना िों",
        "control_method": "visual",
        "frequency": "daily"
    }
   
]
    context = {
        'form': form,
        'json_data': json_data,
        'checkpoint_fields': checkpoint_fields,
        'user_skill_level':user_skill_level,
       }


    return render(request, 'startup/startup_checksheet_form.html',context)

# DetailView to view details of a StartUpCheckSheet entry
class StartUpCheckSheetDetailView(DetailView):
    model = StartUpCheckSheet
    template_name = 'startup/startup_checksheet_detail.html'  # Create this template
    context_object_name = 'check_sheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['json_data'] = [
    {
        "s_no": 1,
        "checkpoint": "Plan के अनसु ार Part assy & Child parts Working Table पर रखें| प्लान के अनसु ार | visual प्रतिदिन",
        "specification": "Part assy & Child parts",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 2,
        "checkpoint": "अपनेकार्स्य थल को साफ करे| कार्स्य थल धलू रदिि िोना चादिए | visual प्रतिदिन",
        "specification": "साफ करे",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 3,
        "checkpoint": "कार्यकरनेसेपिलेWorking table पर सेअनावश्र्क Part / material िटा िें, और उसेउसकी जगि पर रखें| अनावश्र्क Part / material Working Table पर ना िों | visual प्रतिदिन",
        "specification": "Working table पर सेअनावश्र्क Part / material िटा िें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 4,
        "checkpoint": "Dirty tray को लाइन पर use ना करेउसको उसकी तनधायररि जगि पर सफाई के ललए रख िे| Dirty Tray Area visual प्रतिदिन",
        "specification": "Dirty tray को लाइन पर use ना करेउसको उसकी तनधायररि जगि पर सफाई के ललए रख िे",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 5,
        "checkpoint": "चके करेंकक Fixture / Machine Condition OK िों और उसके सभी Connections ठीक िों, Loose ना िों | Fixture / Machine Condition OK, No loose connections visual प्रतिदिन",
        "specification": "Fixture / Machine Condition OK",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 6,
        "checkpoint": "चके करेंकक Fixture / Machine मेंलगेCalibration / Verification Tag की Date Expire ना िों | Verification Tag / Calibration Tag visual प्रतिदिन",
        "specification": "Calibration / Verification Tag की Date Expire ना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 7,
        "checkpoint": "चके करेंकक ESD Wrist Band OK िों | (Where Applicable) लाल / िरा SIGNAL (As per Work instruction) Wrist Band tester प्रतिदिन",
        "specification": "ESD Wrist Band OK",
        "control_method": "Wrist Band tester",
        "frequency": "daily"
    },
    {
        "s_no": 8,
        "checkpoint": "ESD wrist band पिनें| (Where Applicable) कार्यकरिेसमर् Visual प्रतिदिन",
        "specification": "ESD wrist band पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 9,
        "checkpoint": "Face mask पिनें| (Where Applicable) Shop Floor पर उपलब्ध िों| (As per Work instruction) visual प्रतिदिन",
        "specification": "Face mask पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 10,
        "checkpoint": "ESD Jacket & Cap, ESD Gloves/Finger coats पिनें| कार्यकरिेसमर् Visual प्रतिदिन",
        "specification": "ESD Jacket & Cap, ESD Gloves/Finger coats",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 11,
        "checkpoint": "चके करेंकक Red Drawer मेंNG Parts रखनेके ललए Tray उपलब्ध िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Red Drawer मेंNG Parts रखनेके ललए Tray उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 12,
        "checkpoint": "चके करेंकक Drawer मेंजरूरि के अनसु ी र सभी टैग & PPE's उपलब्ध िों | Reject Tag, OK Tag, Abnormal Situation Tag etc. visual प्रतिदिन",
        "specification": "Drawer मेंजरूरि के अनसु ी र सभी टैग & PPE's उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 13,
        "checkpoint": "चके करेंकक Drawer मेंकोई भी अनपुर्ोगी वस्िुना िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Drawer मेंकोई भी अनपुर्ोगी वस्िुना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 14,
        "checkpoint": "चके करेंकक कार्स्य थल पर जरुरि के अनसु ी र सभी Documents उपलब्ध िों | Setup & FPA, Daily monthly Rejection sheet,Control Charts etc. visual प्रतिदिन",
        "specification": "कार्स्य थल पर जरुरि के अनसु ी र सभी Documents उपलब्ध िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 15,
        "checkpoint": "चके करेंकक Line पर OK/NG Master sample उपलब्ध िो और उसकी Date Expire ना िों | कार्यशरूु करनेसेपिले visual प्रतिदिन",
        "specification": "Line पर OK/NG Master sample उपलब्ध िो",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 16,
        "checkpoint": "Tea Break और Lunch मेंबािर जािेसमर् अपनेSetup / System को OFF करके जाएँ| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break और Lunch मेंबािर जािेसमर् अपनेSetup / System को OFF करके जाएँ",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 17,
        "checkpoint": "Tea Break और Lunch मेंबािर जािेसमर् LIGHT को OFF करके जाएँ| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break और Lunch मेंबािर जािेसमर् LIGHT को OFF करके जाएँ",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 18,
        "checkpoint": "Tea Break & Lunch मेंर्दि Shop Floor के अन्िर िैंिो Jacket & Cap पिन कर रखें| Tea break & Lunch visual प्रतिदिन",
        "specification": "Tea Break & Lunch मेंर्दि Shop Floor के अन्िर िैंिो Jacket & Cap पिन कर रखें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 19,
        "checkpoint": "FRL (Pressure gauge) मेंलगी Pin को Push करके 10~12 Sec िक Air को तनकालें, र्दि Air के साथ साथ पानी भी आ रिा िो िो िरुंि अपनेसपु रवाइजर को सचूचि करें| (Where FRL Applicable) OK/NG Visual / Manual प्रतिदिन",
        "specification": "FRL (Pressure gauge) मेंलगी Pin को Push करके 10~12 Sec िक Air को तनकालें, र्दि Air के साथ साथ पानी भी आ रिा िो िो िरुंि अपनेसपु रवाइजर को सचूचि करें",
        "control_method": "Visual / Manual",
        "frequency": "daily"
    },
    {
        "s_no": 20,
        "checkpoint": "चके करेंकक ररजेक्ट िुए Parts के Hand over का िरीका सिी िों | OK/NG सपु रवाइजर के द्वारा प्रतिदिन",
        "specification": "ररजेक्ट िुए Parts के Hand over का िरीका सिी िों",
        "control_method": "Supervisor's verification",
        "frequency": "daily"
    },
    {
        "s_no": 21,
        "checkpoint": "ESD Shoes/Sleepers पिनें| (Where Applicable) Shop Floor पर उपलब्ध िों | visual प्रतिदिन",
        "specification": "ESD Shoes/Sleepers पिन",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 22,
        "checkpoint": "Skill level Card को चके करेंकक उसकी Valid Date Expire ना िों | Shop Floor पर उपलब्ध िों और Valid Date Expire ना िों | visual प्रतिदिन",
        "specification": "Skill level Card को चके करेंकक उसकी Valid Date Expire ना िों",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 23,
        "checkpoint": "चके करेंकक ESD Shoes / Sleepers OK िों | (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "ESD Shoes / Sleepers OK",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 24,
        "checkpoint": "चके करेंकक िर लशफ्ट मेंकार्यशरू करनेसेपिले POGO Pins की ठीक सेसफाई करें| (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "िर लशफ्ट मेंकार्यशरू करनेसेपिले POGO Pins की ठीक सेसफाई करें",
        "control_method": "visual",
        "frequency": "daily"
    },
    {
        "s_no": 25,
        "checkpoint": "कार्यशरू करनेसेपिलेCuring Rack की condition चके करेंकक Timer सेसेटििों और रैक Damage ना िों | (Where Applicable) OK/NG visual प्रतिदिन",
        "specification": "Curing Rack की condition चके करेंकक Timer सेसेटििों और रैक Damage ना िों",
        "control_method": "visual",
        "frequency": "daily"
    }
   
    ]
        check_sheet = self.object
        context['checkpoint_fields'] = []
        for i in range(1, 26):  # Assuming 25 checkpoints
            field_name = f'checkpoint_{i}'
            field_value = getattr(check_sheet, field_name, '')
            context['checkpoint_fields'].append(field_value)
        
        return context
        
# UpdateView to update an existing StartUpCheckSheet entry
class StartUpCheckSheetUpdateView(UpdateView):
    model = StartUpCheckSheet
    form_class = StartUpCheckSheetForm
    template_name = 'startup/startup_checksheet_form.html'  # Reuse the form template
    success_url = reverse_lazy('checksheet_list')  # Redirect to list view after update

# DeleteView to delete a StartUpCheckSheet entry
class StartUpCheckSheetDeleteView(DeleteView):
    model = StartUpCheckSheet
    template_name = 'startup/startup_checksheet_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('checksheet_list')  # Redirect to list view after deletion





# from django.http import JsonResponse
# from .models import MachineLocation

# def get_process_info(request):
#     process_operation_id = request.GET.get('process_operation_id')
#     try:
#         process_operation = MachineLocation.objects.get(id=process_operation_id)
#         data = {
#             'name': process_operation.name,
#             'min_skill_required': process_operation.min_skill_required,
#             # Add any other necessary fields here
#         }
#         return JsonResponse(data)
#     except MachineLocation.DoesNotExist:
#         return JsonResponse({'error': 'Process operation not found'}, status=404)
    
    
    
from .models import MachineLocation  # Assuming you have imported MachineLocation

def get_process_info(request, location_id):
    try:
        machine_location = get_object_or_404(MachineLocation, id=location_id)
        return JsonResponse({'required_skill': machine_location.min_skill_required})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_machine_skill(request, machine_id):
    try:
        machine = get_object_or_404(MachineLocation, id=machine_id)
        try:
            profile = Profile.objects.get(user=request.user)
            user_skill_level = profile.my_skill
        except Profile.DoesNotExist:
            user_skill_level = 0

        return JsonResponse({
            'required_skill': machine.min_skill_required,
            'user_skill_level': user_skill_level
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
# def get_process_info(request, process_operation_id):
#     process_operation = get_object_or_404(ProcessOperation, id=process_operation_id)
#     return JsonResponse({'required_skill': process_operation.min_skill_required})
    
    
    

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PChartData
from .forms import PChartDataForm

class PChartDataListView(ListView):
    model = PChartData
    template_name = 'pchart/pchart_list.html'
    context_object_name = 'pchart_data'

class PChartDataDetailView(DetailView):
    model = PChartData
    template_name = 'pchart/pchart_detail.html'
    context_object_name = 'pchart_data'

class PChartDataCreateView(CreateView):
    model = PChartData
    form_class = PChartDataForm
    template_name = 'pchart/pchart_form.html'
    success_url = reverse_lazy('pchart_list')

class PChartDataUpdateView(UpdateView):
    model = PChartData
    form_class = PChartDataForm
    template_name = 'pchart/pchart_form.html'
    success_url = reverse_lazy('pchart_list')

class PChartDataDeleteView(DeleteView):
    model = PChartData
    template_name = 'pchart/pchart_confirm_delete.html'
    success_url = reverse_lazy('pchart_list')    