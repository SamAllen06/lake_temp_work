module ReadInputParamsMod 
  use fileio_mod, only : fio_open, fio_read, fio_close
  implicit none 
  public :: read_laketemp_params

contains
  subroutine read_laketemp_params()
    use LakeCon 

    integer :: errcode 
    call fio_open(18,'lakeparams.txt', 1) 
    
    call fio_read(18,'betavis',betavis   , errcode=errcode)
    call fio_read(18,'za_lake',za_lake   , errcode=errcode) 
    call fio_read(18,'n2min'  ,n2min     , errcode=errcode)
    call fio_read(18,'tdmax'  ,tdmax     , errcode=errcode) 
    call fio_read(18,'pudz'   ,pudz      , errcode=errcode) 
    call fio_read(18,'mixfact',mixfact  , errcode=errcode) 
    !call fio_read(18,'lakepuddling',lakepuddling,errcode=errcode) 
    !call fio_read(18,'lake_no_ed',lake_no_ed, errcode=errcode) 
    call fio_read(18,'depthcrit', depthcrit,errcode=errcode) 

    call fio_close(18) 
  end subroutine read_laketemp_params

end module ReadInputParamsMod
