// testView.cpp : implementation of the CTestView class
//

#include "stdafx.h"
#include "test.h"

#include "testDoc.h"
#include "testView.h"

#include "math.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CTestView

IMPLEMENT_DYNCREATE(CTestView, CView)

BEGIN_MESSAGE_MAP(CTestView, CView)
	//{{AFX_MSG_MAP(CTestView)
	ON_WM_LBUTTONDOWN()
	ON_WM_MOUSEMOVE()
	ON_WM_RBUTTONDOWN()
	//}}AFX_MSG_MAP
	// Standard printing commands
	ON_COMMAND(ID_FILE_PRINT, CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, CView::OnFilePrintPreview)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CTestView construction/destruction

CTestView::CTestView()
{
	// TODO: add construction code here
	m_LButtonDown = false;

}

CTestView::~CTestView()
{
}

BOOL CTestView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CView::PreCreateWindow(cs);
}

/////////////////////////////////////////////////////////////////////////////
// CTestView drawing

void CTestView::OnDraw(CDC* pDC)
{
	CTestDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	// TODO: add draw code for native data here
}

/////////////////////////////////////////////////////////////////////////////
// CTestView printing

BOOL CTestView::OnPreparePrinting(CPrintInfo* pInfo)
{
	// default preparation
	return DoPreparePrinting(pInfo);
}

void CTestView::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add extra initialization before printing
}

void CTestView::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add cleanup after printing
}

/////////////////////////////////////////////////////////////////////////////
// CTestView diagnostics

#ifdef _DEBUG
void CTestView::AssertValid() const
{
	CView::AssertValid();
}

void CTestView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CTestDoc* CTestView::GetDocument() // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CTestDoc)));
	return (CTestDoc*)m_pDocument;
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CTestView message handlers

void CTestView::OnLButtonDown(UINT nFlags, CPoint point) 
{
	// TODO: Add your message handler code here and/or call default
	m_PointArray.Add(point);
	this->DrawLButtonDown(nFlags,point);
	CView::OnLButtonDown(nFlags, point);
}

void CTestView::OnMouseMove(UINT nFlags, CPoint point) 
{
	// TODO: Add your message handler code here and/or call default
	this->DrawMouseMove(nFlags,point);
	CView::OnMouseMove(nFlags, point);
}

void CTestView::OnRButtonDown(UINT nFlags, CPoint point) 
{
	// TODO: Add your message handler code here and/or call default
	this->DrawRButtonDown(nFlags,point);
	CView::OnRButtonDown(nFlags, point);
}

void CTestView::DrawLButtonDown(UINT nFlags, CPoint point)
{
	SetCursor(m_Cursor);//设置使用光标资源
	
	this->SetCapture();//捕捉鼠标
	//设置开始点和终止点，此时为同一点
	m_StartPoint = point;
	m_EndPoint = point;
	m_LButtonDown = true;//设置鼠标左键按下

}

void CTestView::DrawMouseMove(UINT nFlags, CPoint point)
{
	SetCursor(m_Cursor);//设置使用光标资源
	CClientDC dc(this);//构造设备环境对象

	//判断鼠标移动的同时鼠标左键按下，并且要绘制的是直线段
	if (m_LButtonDown)
	{
		dc.SetROP2(R2_NOT);//设置绘图模式为R2_NOT
		//重新绘制前一个鼠标移动消息处理函数绘制的直线段
		//因为绘图模式的原因，结果是擦除了该线段
		dc.MoveTo(m_StartPoint);
		dc.LineTo(m_EndPoint);
		//绘制新的直线段
		dc.MoveTo(m_StartPoint);
		dc.LineTo(point);
		//保存新的直线段终点
		m_EndPoint = point;
	}

}

void CTestView::DrawRButtonDown(UINT nFlags, CPoint point)
{
	SetCursor(m_Cursor);//设置使用光标资源
	ReleaseCapture();//释放鼠标
	m_LButtonDown = false;
	CClientDC dc(this);
	m_EndPoint = (CPoint)m_PointArray.GetAt(0);
	dc.MoveTo(m_StartPoint);
	dc.LineTo(m_EndPoint);
	EdgeFill();
	m_PointArray.RemoveAll();
}



void CTestView::EdgeFill()
{
	int up,bottom,left,right;
	CPoint p,p2;
	CPoint p1 = m_PointArray.GetAt(0);
	up = bottom = p1.y;
	left = right = p1.x;
	for(int i = 0; i < m_PointArray.GetSize(); i++)
	{
		p = m_PointArray.GetAt(i);
		if(p.x < left) left = p.x;
		if(p.x > right) right = p.x;
		if(p.y < up) up = p.y;
		if(p.y > bottom) bottom = p.y;
	}
	CClientDC dc(this);


/*	COLORREF c1 = RGB(255,255,255),c2 = RGB(255,255,255);
	bool flag = false;
	for( i = up+1 ;i < bottom; i++)
	{
		for( int j = left; j <= right; j++)
		{
			c1 = c2;
			c2 = dc.GetPixel(j,i);
			if(c1 == RGB(255,255,255)&&c2 == RGB(0,0,0))
				flag = !flag;
			if(flag)
				dc.SetPixel(j,i,RGB(255,0,0));
		}
	}*/
	
	COLORREF c1 = RGB(255,0,0);
	int ys,Ixs;
	float xs,dxs;
	for( i = 0 ; i < 2000; i++)
		for(int j = 0; j < 2000; j++)
			MASK[i][j] = false;
	//标志
	for( i = 0; i < m_PointArray.GetSize() ;i++)
	{
		p = m_PointArray.GetAt(i);

		if(i != m_PointArray.GetSize()-1 )
			p1 = m_PointArray.GetAt(i+1);
		else
			p1 = m_PointArray.GetAt(0);

		if(p.y > p1.y)
		{
			p2 = p;
			p = p1;
			p1 = p2;
		}

		xs = p.x;
		(float)dxs = (float)(p1.x - p.x)/(float)(p1.y - p.y);
		for( ys = p.y; ys < p1.y; ys ++)
		{
			
			Ixs = int (xs +0.5);
			MASK[ys][Ixs] = !MASK[ys][Ixs];
			(float)xs = (float)xs + dxs;
		}
		
	}

	//极值点设为false
	for(i = 0; i < m_PointArray.GetSize(); i++)
	{
		p = m_PointArray.GetAt(i);
		if(i != 0 && i != m_PointArray.GetSize() - 1)
		{			
			p1 = m_PointArray.GetAt(i+1);
			p2 = m_PointArray.GetAt(i-1);
		}
		else if( i == 0)
		{
			p1 = m_PointArray.GetAt(i+1);
			p2 = m_PointArray.GetAt(m_PointArray.GetSize()-1);
		}
		else
		{
			p1 = m_PointArray.GetAt(0);
			p2 = m_PointArray.GetAt(i-1);
		}
		if( (p.y < p1.y && p.y < p2.y) || (p.y > p1.y && p.y > p2.y))
			MASK[p.y][p.x] = false;
		else
			MASK[p.y][p.x] = true;
	}



	//填充
	bool inside = false;
	MakeNumber();
	for( i = up+1; i < bottom; i++)
	{
		inside = false;
		for(int j = left; j <= right ;j++)
		{	if(MASK[i][j])
				inside = !inside;
			if(inside)
				if(NUM[j][i])
					dc.SetPixel(j,i,c1);
		}
	}
}




void CTestView::MakeNumber()
{
	int i,j,k,m,n,o;
	k = 2;
	for(i = 0; i < 4000; i++)
		for( j = 0; j < 4000 ;j++)
			NUM[i][j] = false;

	for( m = 0; m < 2000; m += 44*k )
		for( n = 0; n < 2000; n += 23*k)
		{	//0
			for( i = m+3*k; i <= m+11*k ; i++)
				for( j = n+3*k; j <= n+5*k ; j++)
					NUM[i][j] = true;
			for( i = m+ 3*k; i <= m+5*k ; i++)
				for( j = n+5*k; j <= n+18*k ; j++)
					NUM[i][j] = true;
			for( i = m+9*k; i <= m+11*k ; i++)
				for( j = n+5*k; j <= n+18*k ; j++)
					NUM[i][j] = true;
			for( i =m + 3*k; i <= m+11*k ; i++)
				for( j = n+18*k; j <= n+20*k ; j++)
					NUM[i][j] = true;
			o = i-k;
			//6
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+3*k; j <= n+5*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+10*k; j <= n+12*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+18*k; j <= n+20*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k; i <= o+5*k; i++)
				for( j = n+5*k; j <= n+18*k; j++)
					NUM[i][j] = true;
			for(i = o+9*k; i <= o+11*k; i++)
				for( j = n+10*k; j <= n+18*k; j++)
					NUM[i][j] = true;
			o = i-k;
			//1
			for(i = o+6*k; i <= o+8*k; i++)
				for( j = n+3*k; j <= n+20*k; j++)
					NUM[i][j] = true;
			o = i-k;
			//9
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+3*k; j <= n+5*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+10*k; j <= n+12*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+18*k; j <= n+20*k; j++)
					NUM[i][j] = true;
			for(i=o+9*k; i <= o+11*k; i++)
				for( j = n+5*k; j <= n+18*k; j++)
					NUM[i][j] = true;
			for(i = o+3*k; i <= o+5*k; i++)
				for( j = n+3*k; j <= n+12*k; j++)
					NUM[i][j] = true;
/*			//2
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+3*k; j <= n+5*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+10*k; j <= n+12*k; j++)
					NUM[i][j] = true;
			for(i=o+3*k ; i <= o+11*k; i++)
				for( j = n+18*k; j <= n+20*k; j++)
					NUM[i][j] = true;
			for(i=o+9*k; i <= o+11*k; i++)
				for( j = n+5*k; j <= n+12*k; j++)
					NUM[i][j] = true;
			for(i = o+3*k; i <= o+5*k; i++)
				for( j = n+12*k; j <= n+18*k; j++)
					NUM[i][j] = true;*/
		}
}

