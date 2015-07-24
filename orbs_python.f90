
!!модуль предоставляющий функции для работы с hfd.dat
!===================================================
!!get_orb(un,p,q,ni) -- считать орбиталь под номером ni в массивы p,q - большие и
!!малые компоненты орбитали 
!! для python 
!!загрузка радиальных компонент из файла
!!p - большая компонента 
!!q - малая.
!!ni - номер орбитали 
module orbs_python
contains
subroutine get_orb(hfd_dat, ni, maxii, p, q)
implicit none 
integer,intent(in)           :: ni
integer,intent(in)           :: maxii
real(8),intent(out)          :: p(maxii),q(maxii)
real(8)                      :: tmp(2*maxii)
character*(*)               :: hfd_dat
integer                      :: i
    open(unit=241,file=hfd_dat,access='direct',recl=maxii*16)
    read(241,rec=ni+4) (tmp(i),i=1,2*maxii)
    p = tmp(1:maxii)
    q = tmp(maxii+1:)
    close(241)
end subroutine

subroutine get_pseudo_orb(hfj_dat,p,ni, maxii)
implicit none 
integer,intent(in)           :: ni, maxii
real(8),intent(out)          :: p(maxii)
real(8)                      :: tmp(2*maxii)
integer                      :: i
character*(*)               :: hfj_dat
    open(unit=241,file=hfj_dat,access='direct',status='old',recl=maxii*16)
    read(241,rec=ni+4) (tmp(i),i=1,2*maxii)
    p = tmp(1:maxii)
    close(241)
end subroutine

!!загрузка радиальной сетки в массив ro
subroutine getGridFrom(filename, maxii, ro, we, iimax)
implicit none
real(8), intent(out)            :: ro(maxii)
real(8), intent(out)            :: we(maxii)
real(8),allocatable             :: tmp(:), tmp2(:)
integer, intent(in)             :: maxii
integer, intent(out)            :: iimax
character*(*)                   :: filename 
integer                         :: i,k
    allocate(tmp(maxii))
    allocate(tmp2(maxii))
    open(unit=241,file=filename,access='direct',recl=maxii*16)
    read(241,rec=2) (tmp(i),i=1,maxii),(tmp2(i), i=1, maxii)
    close(241)
    k= maxii
    do i=1,maxii
        if (tmp(i)<1d-10.and.i>1) then 
                k=i-1
                exit
        endif
    enddo
    ro(1:k) = tmp(1:k)
    we(1:k) = tmp2(1:k)
    iimax = k
end subroutine
!!загрузка весовой функции в массив v,для корректной работы, должна вызываться
!после getGrid 
!! должны использоваться разные массивы для весов из hfd.dat и hfj.dat

subroutine get_atom_infoFrom(filename, maxii, nn, ll, jj, qq, hgrid, ns) 
implicit none 
integer                                         :: i,k
integer, intent(out)                            :: ns
integer, parameter                              :: nsmax = 200
real(8)                                         :: tmp(2*maxii)
integer, intent(in)                             :: maxii
integer, dimension(nsmax), intent(out) :: nn, ll, jj
real(8), dimension(nsmax), intent(out) :: qq
real(8), intent(out)                            :: hgrid
character*(*)                                   :: filename 
    open(unit=241,file=filename,access='direct',recl=maxii*16)
    read(241,rec=1) (tmp(i),i=1,2*maxii)
    ns = toint(tmp(2))
    hgrid=tmp(6)
    close(241)
    do i=1,ns
      k = 20+(i-1)*6
      nn(i) = toint(tmp(k+1))
      ll(i) = toint(tmp(k+2))
      jj(i) = toint(tmp(k+6))
      qq(i) = tmp(k+3)
    enddo  
    contains
end subroutine 

integer function toInt(x)
    implicit none
    real(8),intent(in) ::x
    toint = int(x+1d-1)
endfunction
end module
